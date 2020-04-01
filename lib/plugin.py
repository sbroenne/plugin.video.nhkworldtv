import random
import re
from datetime import datetime

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

import kodiutils
import nhk_api
import cache_api
import routing
import utils
from episode import Episode

# Initiate constants and plug-in
# When <reuselanguageinvoker>true</reuselanguageinvoker> this only happens
# once per plug-in start!!!

xbmc.log('Retrieving plug-in runtime data')
ADDON = xbmcaddon.Addon()
NHK_ICON = ADDON.getAddonInfo('icon')
NHK_FANART = ADDON.getAddonInfo('fanart')
plugin = routing.Plugin()

# View Modes from the default Estuary skin
VIEW_MODE_INFOWALL = 54
VIEW_MODE_WALL = 500
VIEW_MODE_WIDELIST = 55

if (utils.UNIT_TEST):
    # Run under unit test - set some default data since we will not be able to
    # retrieve data from settings.xml
    MAX_NEWS_DISPLAY_ITEMS = 100
    MAX_ATAGLANCE_DISPLAY_ITEMS = 800
    MAX_PROGRAM_METADATA_CACHE_ITEMS = 1000
    PROGRAM_METADATA_CACHE = utils.get_program_metdadata_cache(
        MAX_PROGRAM_METADATA_CACHE_ITEMS)
    USE_CACHE = True
else:
    xbmc.log('Retrieving plug-in setting')
    # Define how many items should be displayed in News
    MAX_NEWS_DISPLAY_ITEMS = kodiutils.get_setting_as_int("max_news_items")
    # Define how many items should be displayed in At A Glance
    MAX_ATAGLANCE_DISPLAY_ITEMS = kodiutils.get_setting_as_int(
        "max_ataglance_items")
    # Define how many program should be retrieved from meta data cache
    MAX_PROGRAM_METADATA_CACHE_ITEMS = kodiutils.get_setting_as_int(
        "max_program_metadate_cache_items")

    # Episode Cache
    if (kodiutils.get_setting_as_bool('use_backend')):
        PROGRAM_METADATA_CACHE = utils.get_program_metdadata_cache(
            MAX_PROGRAM_METADATA_CACHE_ITEMS)
        USE_CACHE = True
    else:
        PROGRAM_METADATA_CACHE = {'CACHE_DISABLED', 'CASHHNG DISABLED'}
        USE_CACHE = False


# Start page of the plug-in
@plugin.route('/')
def index():
    xbmc.log('Creating Main Menu')

    # Add menus
    
    add_live_stream_menu_item()
    add_on_demand_menu_item()
    add_live_schedule_menu_item()
    add_top_stories_menu_item()
    add_ataglance_menu_item()

    # News Programs
    art = {
        'thumb':
        'https://www3.nhk.or.jp/nhkworld/upld/thumbnails/en/news/programs/1001_2.jpg',
        'fanart':
        'https://www3.nhk.or.jp/nhkworld/common/assets/news/images/programs/newsline_2020.jpg'
    }
    li = xbmcgui.ListItem(kodiutils.get_string(30080))
    info_labels = {}
    info_labels['mediatype'] = 'episode'
    info_labels['Plot'] = kodiutils.get_string(30081)
    li.setInfo('video', info_labels)
    li.addStreamInfo('video', kodiutils.get_SD_video_info())
    li.setArt(art)
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(news_programs_index), li, True)

    # Set-up view
    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.endOfDirectory(plugin.handle)
    return (True)


#
# Top Stories
#


#  Menu item
def add_top_stories_menu_item():
    xbmc.log('Adding top stories menu item')

    # Getting top story
    featured_news = utils.get_json(nhk_api.rest_url['homepage_news'],
                                   False)['data'][0]
    thumbnails = featured_news['thumbnails']

    episode = Episode()
    if (thumbnails is None):
        # Featured news does not have a thumbnail
        episode.thumb = NHK_ICON
        episode.fanart = NHK_FANART
    else:
        episode.thumb = thumbnails['small']
        episode.fanart = thumbnails['middle']

    episode.title = kodiutils.get_string(30010)

    # Create the plot field
    episode.plot = kodiutils.get_string(30012).format(
        featured_news['title'], featured_news['description'])

    # Create the directory itemn
    episode.video_info = kodiutils.get_SD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(top_stories_index),
                                episode.kodi_list_item, True)
    return (True)


# List
@plugin.route('/news/top_stories/index')
def top_stories_index():
    xbmc.log('Displaying Top Stories Index')
    api_result_json = utils.get_json(nhk_api.rest_url['homepage_news'], False)
    max_row_count = MAX_NEWS_DISPLAY_ITEMS
    result_row_count = len(api_result_json['data'])
    # Only display MAX ROWS
    if (result_row_count < max_row_count):
        max_row_count = result_row_count

    for row_count in range(0, max_row_count - 1):
        row = api_result_json['data'][row_count]

        episode = Episode()
        title = row['title']
        news_id = row['id']

        thumbnails = row['thumbnails']

        if (thumbnails is None):
            # Featured news does not have a thumbnail
            episode.thumb = NHK_ICON
            episode.fanart = NHK_FANART
        else:
            episode.thumb = thumbnails['small']
            episode.fanart = thumbnails['middle']

        episode.broadcast_start_date = row['updated_at']
        episode.date = episode.broadcast_start_date

        date_delta = datetime.now() - episode.broadcast_start_date
        date_delta_minutes = date_delta.seconds / 60
        date_delta_hours = date_delta_minutes / 60
        if (date_delta.days > 0):
            # Show as absolute date
            time_difference = episode.broadcast_start_date.strftime(
                '%A, %b %d, %H:%M')
        elif (date_delta_hours < 1):
            # Show in minutes
            time_difference = kodiutils.get_string(30062).format(
                date_delta_minutes)
        elif (date_delta_hours == 1):
            # Show as hour
            time_difference = kodiutils.get_string(30060).format(
                date_delta_hours)
        else:
            # Show as hours (plural)
            time_difference = kodiutils.get_string(30061).format(
                date_delta_hours)
        if row['videos'] is not None:
            video = row['videos']
            # Top stories that have a video attached to them
            episode.title = kodiutils.get_string(30070).format(title)
            episode.vod_id = news_id
            episode.duration = video['duration']
            minutes = int(episode.duration / 60)
            seconds = episode.duration - (minutes * 60)
            duration_text = '{0}m {1}'.format(minutes, seconds)

            episode.plot = u'{0} | {1}\n\n{2}'.format(duration_text,
                                                      time_difference,
                                                      row['description'])
            episode.video_info = kodiutils.get_SD_video_info()
            episode.IsPlayable = True

            api_url = utils.get_NHK_website_url(video['config'])
            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(play_news_item, api_url, episode.vod_id, 'news',
                               title), episode.kodi_list_item, False)

        else:
            # No video attached to it
            episode.title = title
            # Get detailed news information
            api_url = nhk_api.rest_url['news_detail'].format(news_id)
            news_detail_json = utils.get_json(api_url)['data']
            detail = news_detail_json['detail']
            detail = detail.replace('<br />', '\n')
            detail = detail.replace('\n\n', '\n')
            episode.plot = u'{0}\n\n{1}'.format(time_difference, detail)
            thumbnails = news_detail_json['thumbnails']
            if (thumbnails is not None):
                episode.thumb = thumbnails['small']
                episode.fanart = thumbnails['middle']
            episode.IsPlayable = False
            xbmcplugin.addDirectoryItem(plugin.handle, None,
                                        episode.kodi_list_item, False)

    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_NONE,
                                              "Descending")

    # Used for unit testing
    # only successfull if we processed at least top story
    if (row_count > 0):
        return (row_count)
    else:
        return (0)


#
# At a glance
#


#  Menu item
def add_ataglance_menu_item():
    xbmc.log('Adding at a glance menu item')

    # Getting firststory
    featured_news = utils.get_json(
        nhk_api.rest_url['get_news_ataglance'])['data'][0]
    thumbnails = featured_news['image']

    episode = Episode()
    if (thumbnails is None):
        # Featured news does not have a thumbnail
        episode.thumb = NHK_ICON
        episode.fanart = NHK_FANART
    else:
        episode.thumb = thumbnails['list_sp']
        episode.fanart = thumbnails['main_pc']

    episode.title = kodiutils.get_string(30015)

    # Create the plot field
    episode.plot = kodiutils.get_string(30012).format(
        featured_news['title'], featured_news['description'])

    # Create the directory itemn
    episode.video_info = kodiutils.get_SD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(ataglance_index),
                                episode.kodi_list_item, True)
    return (True)


# List
@plugin.route('/news/ataglance/index')
def ataglance_index():
    xbmc.log('Displaying At a Glance Index')
    api_result_json = utils.get_json(nhk_api.rest_url['get_news_ataglance'])
    max_row_count = MAX_ATAGLANCE_DISPLAY_ITEMS
    result_row_count = len(api_result_json['data'])
    # Only display MAX ROWS
    if (result_row_count < max_row_count):
        max_row_count = result_row_count

    for row_count in range(0, max_row_count - 1):
        row = api_result_json['data'][row_count]

        episode = Episode()
        title = row['title']

        thumbnails = row['image']

        if (thumbnails is None):
            # Featured news does not have a thumbnail
            episode.thumb = NHK_ICON
            episode.fanart = NHK_FANART
        else:
            if (thumbnails['list_sp'] is not None):
                episode.thumb = thumbnails['list_sp']
            else:
                episode.thumb = thumbnails['list_pc']

            episode.fanart = thumbnails['main_pc']

        episode.broadcast_start_date = row['posted_at']
        episode.date = episode.broadcast_start_date

        episode.title = title
        vod_id = row['id']
        episode.vod_id = vod_id
        episode.duration = row['video']['duration']
        if (episode.duration is not None):
            minutes = int(episode.duration / 60)
            seconds = episode.duration - (minutes * 60)
            duration_text = '{0}m {1}'.format(minutes, seconds)
            episode.plot = u'{0}\n\n{1}'.format(duration_text,
                                                row['description'])
        else:
            episode.plot = row['description']

        episode.video_info = kodiutils.get_SD_video_info()
        episode.IsPlayable = True
        api_url = utils.get_NHK_website_url(row['video']['config'])
        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(play_news_item, api_url, episode.vod_id,
                           'ataglance', episode.title), episode.kodi_list_item,
            False)

    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_NONE,
                                              "Descending")

    # Used for unit testing
    # only successfull if we processed at least top story
    if (row_count > 0):
        return (row_count)
    else:
        return (0)


# News Programs
@plugin.route('/news/programs/index')
def news_programs_index():
    xbmc.log('Displaying At News Index')
    api_result_json = utils.get_json(
        nhk_api.rest_url['news_program_config'])['config']['programs']
    row_count = 0
    for row in api_result_json:
        row_count = row_count + 1
        episode = Episode()
        news_program_id = row['id']
        vod_id = u'news_program_{0}'.format(news_program_id)
        episode.vod_id = vod_id
        episode.title = row['name']
        episode.fanart = row['image']
        episode.thumb = row['image']
        api_url = nhk_api.rest_url['news_program_xml'].format(news_program_id)
        episode.video_info = kodiutils.get_SD_video_info()
        episode.IsPlayable = True
        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(play_news_item, api_url, episode.vod_id,
                           'news_program', episode.title),
            episode.kodi_list_item, False)

    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_NONE,
                                              "Descending")

    # Used for unit testing
    # only successfull if we processed at least top story
    if (row_count > 0):
        return (row_count)
    else:
        return (0)


# Add on-demand menu item
def add_on_demand_menu_item():
    xbmc.log('Adding on-demand menu item')
    # Getting random on-demand episode to show
    featured_episodes = utils.get_json(
        nhk_api.rest_url['homepage_ondemand'])['data']['items']
    no_of_epsisodes = len(featured_episodes)
    pgm_title = None
    try_count = 0
    # Fine a valid episode to highlight
    while (pgm_title is None):
        try_count = try_count + 1
        xbmc.log(
            'Determening if random episode has a valid title. Try count:{0}'.
            format(try_count))
        featured_episode = random.randint(0, no_of_epsisodes - 1)
        program_json = featured_episodes[featured_episode]
        pgm_title = program_json['pgm_title_clean']

    episode = Episode()
    episode.title = kodiutils.get_string(30020)
    episode.plot = kodiutils.get_string(30022).format(
        utils.get_episode_name(pgm_title, program_json['subtitle']))
    episode.thumb = program_json['image_sp']
    episode.fanart = program_json['image_pc']

    # Create the directory itemn
    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_index),
                                episode.kodi_list_item, True)
    return (True)


# Add live stream menu item
def add_live_stream_menu_item():
    xbmc.log('Adding live stream menu item')
    xbmc.log('Retrieving live stream next shows')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'],
                                  False)['channel']['item']

    # Add live stream text
    episode = Episode()
    episode.title = kodiutils.get_string(30030)

    # Currently playing
    row = program_json[0]

    # Schedule Information
    episode.broadcast_start_date = row['pubDate']
    episode.broadcast_end_date = row['endDate']
    episode.thumb = row['thumbnail_s']
    episode.fanart = row['thumbnail']
    episode.IsPlayable = True
    episode.url = nhk_api.rest_url['live_stream_url']

    # Title and Description
    full_title = u'{0}\n\n{1}'.format(row['title'], row['description'])
    episode.plot = u'{0}-{1}: {2}'.format(
        episode.broadcast_start_date.strftime('%H:%M'),
        episode.broadcast_end_date.strftime('%H:%M'), full_title)

    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle, episode.url,
                                episode.kodi_list_item, False)
    return (True)


#
# Live schedule
#


# Menu item
def add_live_schedule_menu_item():
    xbmc.log('Adding live schedule menu item')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'],
                                  False)['channel']['item']

    # Featured Episode
    no_of_epsisodes = len(program_json)
    featured_episode = random.randint(1, no_of_epsisodes - 1)
    row = program_json[featured_episode]

    # Add live-schedule text
    episode = Episode()
    episode.title = kodiutils.get_string(30036)

    # Schedule Information
    episode.broadcast_start_date = row['pubDate']
    episode.broadcast_end_date = row['endDate']
    episode.date = episode.broadcast_start_date
    episode.thumb = row['thumbnail_s']
    episode.fanart = row['thumbnail']

    title = u'{0}-{1}: {2}'.format(
        episode.broadcast_start_date.strftime('%H:%M'),
        episode.broadcast_end_date.strftime('%H:%M'), row['title'])
    episode.plot = '{0}\n\n{1}'.format(
        kodiutils.get_string(30022).format(title), row['description'])

    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(live_schedule_index),
                                episode.kodi_list_item, True)
    return (True)


#
# List
#


@plugin.route('/live_schedule/index')
def live_schedule_index():
    xbmc.log('Adding live schedule inde')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'],
                                  False)['channel']['item']

    row_count = 0
    for row in program_json:
        row_count = row_count + 1

        episode = Episode()
        # Schedule Information
        episode.broadcast_start_date = row['pubDate']
        episode.broadcast_end_date = row['endDate']
        episode.date = episode.broadcast_start_date
        duration_diff = episode.broadcast_start_date \
            - episode.broadcast_end_date
        episode.duration = duration_diff.seconds

        # Live program
        episode.thumb = row['thumbnail_s']
        episode.fanart = row['thumbnail']
        episode_name = utils.get_episode_name(row['title'], row['subtitle'])
        title = u'{0}-{1}: {2}'.format(
            episode.broadcast_start_date.strftime('%H:%M'),
            episode.broadcast_end_date.strftime('%H:%M'), episode_name)

        vod_id = row['vod_id']
        episode.vod_id = vod_id
        if (len(vod_id) > 0):
            # Can play on-demand
            episode.IsPlayable = True
            episode.title = kodiutils.get_string(30070).format(title)
        else:
            episode.title = title

        episode.plot = u'{0}\n\n{1}'.format(episode_name, row['description'])

        if (episode.IsPlayable):
            # Display the playable episode
            add_playable_episode_directory_item(episode)
        else:
            # Simply display text
            xbmcplugin.addDirectoryItem(plugin.handle, None,
                                        episode.kodi_list_item, False)

    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_WIDELIST,
                                              xbmcplugin.SORT_METHOD_NONE)

    return row_count


#
# Video On Demand Mennu
#


@plugin.route('/vod/index')
def vod_index():
    xbmc.log('Creating Video On Demand Menu')
    art = {'thumb': NHK_ICON, 'fanart': NHK_FANART}
    # Programs
    li = xbmcgui.ListItem(kodiutils.get_string(30040))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_programs),
                                li, True)
    # Categories
    li = xbmcgui.ListItem(kodiutils.get_string(30041))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_categories),
                                li, True)
    # Playlists
    li = xbmcgui.ListItem(kodiutils.get_string(30042))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_playlists),
                                li, True)
    # Latest Episodes
    li = xbmcgui.ListItem(kodiutils.get_string(30043))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list,
                       nhk_api.rest_url['get_latest_episodes'], 0,
                       xbmcplugin.SORT_METHOD_DATE), li, True)
    # Most Watched
    li = xbmcgui.ListItem(kodiutils.get_string(30044))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list,
                       nhk_api.rest_url['get_most_watched_episodes'], 0,
                       xbmcplugin.SORT_METHOD_NONE), li, True)
    # All
    li = xbmcgui.ListItem(kodiutils.get_string(30045))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list, nhk_api.rest_url['get_all_episodes'],
                       0, xbmcplugin.SORT_METHOD_LABEL), li, True)
    kodiutils.set_view_mode(VIEW_MODE_WIDELIST)
    xbmcplugin.endOfDirectory(plugin.handle)
    return (True)


# By Program (Programs Tab on NHK World Site)
@plugin.route('/vod/programs/')
def vod_programs():

    program_json = utils.get_json(
        nhk_api.rest_url['get_programs'])['vod_programs']['programs']
    row_count = 0

    for index in program_json:
        row = program_json[index]
        row_count = row_count + 1
        total_episodes = int(row['total_episode'])
        if total_episodes > 0:
            # Only show programs that have at lease on episode
            episode = Episode()
            episode.title = utils.get_episodelist_title(
                row['title_clean'], total_episodes)
            episode.plot = row['description_clean']
            episode.thumb = row['image']
            episode.fanart = row['image_l']
            episode.video_info = kodiutils.get_1080_HD_video_info()

            # Create the directory item
            api_url = nhk_api.rest_url['get_programs_episode_list'].format(
                index)
            xbmc.log('Creating Directory Item {0} - {1}'.format(
                api_url, episode.title.encode('ascii', 'ignore')))

            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(vod_episode_list, api_url, 1,
                               xbmcplugin.SORT_METHOD_DATE),
                episode.kodi_list_item, True)

    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_LABEL)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return (api_url)
    else:
        return (None)


# Categories


@plugin.route('/vod/categories/')
def vod_categories():

    api_result_json = utils.get_json(nhk_api.rest_url['get_categories'])
    row_count = 0
    for row in api_result_json['vod_categories']:
        row_count = row_count + 1
        episode = Episode()

        episode.title = utils.get_episodelist_title(row['name'], row['count'])
        episode.absolute_image_url = True
        episode.thumb = row['icon_l']
        episode.fanart = row['icon_l']
        episode.video_info = kodiutils.get_1080_HD_video_info()

        # Create the directory item
        categoryId = row['category_id']
        api_url = nhk_api.rest_url['get_categories_episode_list'].format(
            categoryId)
        xbmc.log('Creating Directory Item {0} - {1}'.format(
            api_url, episode.title.encode('ascii', 'ignore')))
        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(vod_episode_list, api_url, 0,
                           xbmcplugin.SORT_METHOD_DATE),
            episode.kodi_list_item, True)

    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_WALL,
                                              xbmcplugin.SORT_METHOD_LABEL)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return (api_url)
    else:
        return (None)


# Playlists


@plugin.route('/vod/playlists/')
def vod_playlists():

    api_result_json = utils.get_json(nhk_api.rest_url['get_playlists'])
    row_count = 0
    for row in api_result_json['data']['playlist']:
        row_count = row_count + 1

        episode = Episode()
        episode.title = utils.get_episodelist_title(row['title_clean'],
                                                    row['track_total'])
        episode.thumb = row['image_square']
        episode.fanart = row['image_square']

        playlistId = row['playlist_id']
        api_url = nhk_api.rest_url['get_playlists_episode_list'].format(
            playlistId)

        xbmc.log('Creating Directory Item {0} - {1}'.format(
            api_url, episode.title.encode('ascii', 'ignore')))

        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(vod_episode_list, api_url, 0,
                           xbmcplugin.SORT_METHOD_LABEL),
            episode.kodi_list_item, True)

    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_WALL,
                                              xbmcplugin.SORT_METHOD_LABEL)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return (api_url)
    else:
        return (None)


def add_playable_episode_directory_item(episode, enforce_cache=False):
    """ Add a Kodi directory item for a playable episode """
    # If the vod_id is in cache and cache is being used,
    # diretly add the URL otherwise dynmaically resolve it
    # via show_epsisode()
    #
    # Use the cache backend or not
    if (enforce_cache):
        use_backend = True
    else:
        use_backend = USE_CACHE

    if (use_backend):
        if (episode.vod_id in PROGRAM_METADATA_CACHE):
            cached_episode = PROGRAM_METADATA_CACHE[episode.vod_id]
            # In cache - display directly
            episode.url = nhk_api.rest_url['episode_url'].format(
                cached_episode["PlayPath"])
            episode.aspect = cached_episode['Aspect']
            episode.width = cached_episode['Width']
            episode.height = cached_episode['Height']
            episode.onair = cached_episode['OnAir']
            xbmcplugin.addDirectoryItem(plugin.handle, episode.url,
                                        episode.kodi_list_item)
            return (True)

    # Not in cache - need to be resolve dynmaically

    xbmcplugin.addDirectoryItem(
        plugin.handle, plugin.url_for(play_vod_episode, episode.vod_id),
        episode.kodi_list_item)
    return (True)


# Video On Demand - Episode List
@plugin.route(
    '/vod/episode_list/<path:api_url>/<show_only_subtitle>/<sort_method>/')
def vod_episode_list(api_url,
                     show_only_subtitle,
                     sort_method,
                     enforceCache=False):
    xbmc.log('Displaying Episode List for URL: {0} - {1}'.format(
        api_url, show_only_subtitle))
    api_result_json = utils.get_json(api_url)['data']

    if ('episodes' in api_result_json):
        # "Normal" episode list
        program_json = api_result_json['episodes']
    elif ('playlist' in api_result_json):
        # Episode List that is generated by the PlayList API
        program_json = api_result_json['playlist'][0]['track']
    else:
        # Unknown source, abort
        return None

    row_count = 0
    for row in program_json:
        row_count = row_count + 1
        episode = Episode()
        episode.IsPlayable = True
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if int(show_only_subtitle) == 1:
            # Show only subtitle
            if len(subtitle) > 0:
                # There is a subtitle, use it
                episode_name = subtitle
            else:
                # Use the title instead of the subtitle
                episode_name = title
        else:
            # Show complete title
            if len(title) == 0:
                # Use the subtitle as the episode name
                # because there is no title
                episode_name = subtitle
            else:
                # Use the full episode name
                episode_name = utils.get_episode_name(title, subtitle)

        episode.title = episode_name
        description = row['description_clean']
        episode.thumb = row['image']
        episode.fanart = row['image_l']
        episode.vod_id = row['vod_id']
        episode.pgm_no = row['pgm_no']
        episode.duration = row['movie_duration']

        # Check if we have an aired date
        broadcast_start_timestamp = row['onair']

        if (broadcast_start_timestamp is not None):
            episode.broadcast_start_date = broadcast_start_timestamp
            episode.broadcast_end_date = row['vod_to']
            episode.date = episode.broadcast_start_date
            episode.plot = kodiutils.get_string(30050).format(
                episode.broadcast_start_date.strftime('%Y-%m-%d'),
                episode.broadcast_end_date.strftime('%Y-%m-%d'), description)
        else:
            episode.plot = description

        # Add the current episode directory item
        add_playable_episode_directory_item(episode)

    sort_method = int(sort_method)
    kodiutils.set_video_directory_information(plugin.handle,
                                              VIEW_MODE_INFOWALL, sort_method)

    # Used for unit testing
    # only successfull hif we processed at least one episode
    if (row_count > 0):
        return (episode)
    else:
        return (None)


# Video On Demand - Play Episode
@plugin.route('/vod/play_episode/<vod_id>/')
def play_vod_episode(vod_id, enforce_cache=False):

    xbmc.log('VOD_ID: {0}'.format(vod_id))
    xbmc.log('ENFORCE CACHE: {0}'.format(enforce_cache))

    if (enforce_cache):
        use_backend = True
    else:
        use_backend = USE_CACHE

    episode = Episode()
    episode.vod_id = vod_id
    episode.IsPlayable = True

    if (use_backend):
        # Use NHK World TV Cloud Service to speed-up start of episode playback
        # The service runs on Azure in West Europe but should still
        # speed up the lookup process dramatically
        # since it uses a pre-loaded cache
        xbmc.log('Using Cloud Service to retrieve vod_id: {0}'.format(vod_id))
        cached_episode = utils.get_json(
            cache_api.rest_url['cache_get_program'].format(vod_id))
        episode.title = cached_episode['Title']
        episode.plot = cached_episode['Plot']
        episode.pgm_no = cached_episode['PgmNo']
        if (cached_episode['Duration'] is not None):
            episode.duration = cached_episode['Duration']
        episode.url = nhk_api.rest_url['episode_url'].format(
            cached_episode['PlayPath'])
        episode.aspect = cached_episode['Aspect']
        episode.width = cached_episode['Width']
        episode.height = cached_episode['Height']
        if (cached_episode['OnAir'] is not None):
            episode.onair = cached_episode['OnAir']
            episode.broadcast_start_date = cached_episode['OnAir']
            episode.date = episode.broadcast_start_date
        if (cached_episode['Duration'] is not None):
            episode.duration = cached_episode['Duration']
    else:
        # Get result from NHK - slow
        xbmc.log('Using Player.js to retrieve vod_id: {0}'.format(vod_id))
        r = utils.get_url(nhk_api.rest_url['player_url'].format(
            vod_id, vod_id))
        playerJS = r.text
        # Parse the output of the Player JS file for the UUID of the episode
        uuid_match = re.compile("'data-de-program-uuid','(.+?)'").findall(
            playerJS)
        program_Uuid = uuid_match[0]

        # Get episode detail
        episode_detail = utils.get_json(
            nhk_api.rest_url['get_episode_detail'].format(
                vod_id))['data']['episodes'][0]
        episode.title = episode_detail['title_clean']
        episode.broadcast_start_date = episode_detail['onair']
        episode.date = episode.broadcast_start_date
        episode.plot = episode_detail['description_clean']
        episode.pgm_no = episode_detail['pgm_no']
        episode.duration = episode_detail['movie_duration']

        # Get episode URL and video information
        video_url = nhk_api.rest_url['video_url'].format(program_Uuid)
        reference_file_json = utils.get_json(video_url)['response'][
            'WsProgramResponse']['program']['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        episode.url = nhk_api.rest_url['episode_url'].format(play_path)
        episode.aspect = reference_file_json['aspectRatio']
        episode.width = reference_file_json['videoWidth']
        episode.height = reference_file_json['videoHeight']

    xbmcplugin.setResolvedUrl(plugin.handle, True, episode.kodi_list_item)
    return (episode.url)


#  Play News or At A Glance Item
@plugin.route(
    '/news/play_news_item/<path:api_url>/<news_id>/<item_type>/<title>/')
def play_news_item(api_url, news_id, item_type, title):
    """ Play a news item - can either be 'news' or 'ataglance' or 'news_program' """
    xbmc.log('ITEM_TYPE: {0}'.format(item_type))
    xbmc.log('API_URL: {0}'.format(api_url))
    xbmc.log('NEWS_ID: {0}'.format(news_id))
    xbmc.log('TITLE: {0}'.format(title))

    video_xml = utils.get_url(api_url).text
    if (item_type == 'news'):
        play_path = nhk_api.rest_url['news_video_url'].format(
            utils.get_top_stories_play_path(video_xml))
    elif (item_type == 'ataglance'):
        play_path = nhk_api.rest_url['ataglance_video_url'].format(
            utils.get_ataglance_play_path(video_xml))
    elif (item_type == 'news_program'):
        play_path = nhk_api.rest_url['news_programs_video_url'].format(
            utils.get_news_program_play_path(video_xml))
    else:
        return (False)

    xbmc.log('Play Path: {0}'.format(play_path))
    episode = Episode()
    episode.vod_id = news_id
    episode.title = title
    episode.url = play_path
    episode.video_info = kodiutils.get_SD_video_info()
    episode.IsPlayable = True

    xbmcplugin.setResolvedUrl(plugin.handle, True, episode.kodi_list_item)
    return (True)


#
# Main loop
#


def run():
    plugin.run()
