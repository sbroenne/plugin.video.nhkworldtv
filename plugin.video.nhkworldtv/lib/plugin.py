# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
import re
import xml.etree.ElementTree as ET
from builtins import range

import routing
from kodi_six import xbmc, xbmcaddon, xbmcgui, xbmcplugin

from . import cache_api, kodiutils, nhk_api, utils
from .episode import Episode

# Initiate constants and plug-in
# When <reuselanguageinvoker>true</reuselanguageinvoker> this only happens
# once per plug-in start!!!

xbmc.log('Retrieving plug-in runtime data')
ADDON = xbmcaddon.Addon()
NHK_ICON = ADDON.getAddonInfo('icon')
NHK_FANART = ADDON.getAddonInfo('fanart')
plugin = routing.Plugin()

if (utils.UNIT_TEST):
    # Run under unit test - set some default data since we will not be able to
    # retrieve data from settings.xml
    MAX_NEWS_DISPLAY_ITEMS = 20
    MAX_ATAGLANCE_DISPLAY_ITEMS = 800
    MAX_PROGRAM_METADATA_CACHE_ITEMS = 2000
    PROGRAM_METADATA_CACHE = utils.get_program_metdadata_cache(
        MAX_PROGRAM_METADATA_CACHE_ITEMS)
    USE_CACHE = True
else:
    xbmc.log('Retrieving plug-in setting')
    # Define how many items should be displayed in News
    MAX_NEWS_DISPLAY_ITEMS = ADDON.getSettingInt("max_news_items")
    # Define how many items should be displayed in At A Glance
    MAX_ATAGLANCE_DISPLAY_ITEMS = ADDON.getSettingInt("max_ataglance_items")
    # Define how many program should be retrieved from meta data cache
    MAX_PROGRAM_METADATA_CACHE_ITEMS = ADDON.getSettingInt(
        "max_program_metadate_cache_items")

    # Episode Cache
    if (ADDON.getSettingBool('use_backend')):
        PROGRAM_METADATA_CACHE = utils.get_program_metdadata_cache(
            MAX_PROGRAM_METADATA_CACHE_ITEMS)
        USE_CACHE = True
    else:
        PROGRAM_METADATA_CACHE = {'CACHE_DISABLED', 'CACHE DISABLED'}
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
    add_news_programs_menu_item()
    # Set-up view
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_UNSORTED,
                                              'videos')
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
@plugin.route('/top_stories/index')
def top_stories_index():
    xbmc.log('Displaying Top Stories Index')
    api_result_json = utils.get_json(nhk_api.rest_url['homepage_news'], False)
    max_row_count = MAX_NEWS_DISPLAY_ITEMS
    result_row_count = len(api_result_json['data'])
    episodes = []
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
        if row['videos'] is not None:
            video = row['videos']
            # Top stories that have a video attached to them
            episode.title = kodiutils.get_string(30070).format(title)
            episode.vod_id = news_id
            episode.duration = video['duration']
            episode.plot_include_time_difference = True
            episode.plot = row['description']
            episode.video_info = kodiutils.get_SD_video_info()
            episode.IsPlayable = True

            api_url = utils.get_NHK_website_url(video['config'])
            episodes.append(
                (plugin.url_for(play_news_item, api_url, episode.vod_id,
                                'news', title), episode.kodi_list_item, False))

        else:
            # No video attached to it
            episode.title = title
            # Get detailed news information
            api_url = nhk_api.rest_url['news_detail'].format(news_id)
            news_detail_json = utils.get_json(api_url)['data']
            detail = news_detail_json['detail']
            detail = detail.replace('<br />', '\n')
            detail = detail.replace('\n\n', '\n')
            episode.plot_include_time_difference = True
            episode.plot = detail
            thumbnails = news_detail_json['thumbnails']
            if (thumbnails is not None):
                episode.thumb = thumbnails['small']
                episode.fanart = thumbnails['middle']
            episode.IsPlayable = False
            episodes.append((None, episode.kodi_list_item, False))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_UNSORTED,
                                              'videos')

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
@plugin.route('/ataglance/index')
def ataglance_index():
    xbmc.log('Displaying At a Glance Index')
    api_result_json = utils.get_json(nhk_api.rest_url['get_news_ataglance'])
    max_row_count = MAX_ATAGLANCE_DISPLAY_ITEMS
    result_row_count = len(api_result_json['data'])
    episodes = []
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
        episode.title = title
        vod_id = row['id']
        episode.vod_id = vod_id
        episode.duration = row['video']['duration']
        if (episode.duration is not None):
            episode.plot_include_time_difference = True
            episode.plot = row['description']
        else:
            episode.plot_include_time_difference = True
            episode.plot = row['description']

        episode.video_info = kodiutils.get_SD_video_info()
        episode.IsPlayable = True
        api_url = utils.get_NHK_website_url(row['video']['config'])
        episodes.append(
            (plugin.url_for(play_news_item, api_url, episode.vod_id,
                            'ataglance',
                            episode.title), episode.kodi_list_item, False))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_UNSORTED,
                                              'videos')

    # Used for unit testing
    # only successfull if we processed at least top story
    if (row_count > 0):
        return (row_count)
    else:
        return (0)


#
# News Programs
#


# Menu item
def add_news_programs_menu_item():
    art = {
        'thumb':
        'https://www3.nhk.or.jp/nhkworld/upld/thumbnails/en/' +
        'news/programs/1001_2.jpg',
        'fanart':
        'https://www3.nhk.or.jp/nhkworld/common/assets/news/images/programs/' +
        'newsline_2020.jpg'
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
    return (True)


# List
@plugin.route('/news/programs/index')
def news_programs_index():
    xbmc.log('Displaying At News Index')
    api_result_json = utils.get_json(nhk_api.rest_url['news_program_config'],
                                     False)
    news_programs = api_result_json['config']['programs']
    row_count = 0
    episodes = []
    for news_program in news_programs:
        row_count = row_count + 1
        news_program_id = news_program['id']
        api_url = nhk_api.rest_url['news_program_xml'].format(news_program_id)
        news_program_xml = utils.get_url(api_url, False).text
        try:
            root = ET.fromstring(news_program_xml)
            success = True
        except ET.ParseError:
            xbmc.log('Couldnt load Program XML {0}'.format(news_program_id))
            success = False

        if (success):
            play_path = nhk_api.rest_url['news_programs_video_url'].format(
                utils.get_news_program_play_path(root.find('file.high').text))
            episode = Episode()
            vod_id = 'news_program_{0}'.format(news_program_id)
            episode.vod_id = vod_id

            # Extract the Title
            description = root.find('description').text
            episode.title = description.split('<br />', 1)[0]
            # Extract the broadcast time and convert it to local time
            episode.broadcast_start_date = utils.get_timestamp_from_datestring(
                (description.split('<br />', 1)[1]).strip())
            episode.plot_include_time_difference = True
            episode.plot = ''
            episode.fanart = news_program['image']
            episode.thumb = news_program['image']
            episode.duration = root.find('media.time').text
            episode.video_info = kodiutils.get_SD_video_info()
            episode.IsPlayable = True
            episodes.append((play_path, episode.kodi_list_item, False))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_UNSORTED,
                                              'videos')

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
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'],
                                  False)['channel']['item']

    # Add live stream text
    episode = Episode()
    episode.title = kodiutils.get_string(30030)

    # Currently playing
    row = program_json[0]

    # Schedule Information
    episode.thumb = row['thumbnail_s']
    episode.fanart = row['thumbnail']
    episode.IsPlayable = True
    episode.playcount = 0
    episode.url = nhk_api.rest_url['live_stream_url']

    # Title and Description
    plot = '{0}\n\n{1}'.format(row['title'], row['description'])
    episode.plot = plot

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
    episode.thumb = row['thumbnail_s']
    episode.fanart = row['thumbnail']

    title = utils.get_schedule_title(episode.broadcast_start_date,
                                     episode.broadcast_end_date, row['title'])
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
    xbmc.log('Adding live schedule index')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'],
                                  False)['channel']['item']
    row_count = 0
    episodes = []
    for row in program_json:
        row_count = row_count + 1

        episode = Episode()
        # Schedule Information
        episode.broadcast_start_date = row['pubDate']
        episode.broadcast_end_date = row['endDate']

        # Live program
        episode.thumb = row['thumbnail_s']
        episode.fanart = row['thumbnail']
        episode_name = utils.get_episode_name(row['title'], row['subtitle'])
        title = utils.get_schedule_title(episode.broadcast_start_date,
                                         episode.broadcast_end_date,
                                         episode_name)

        vod_id = row['vod_id']
        episode.vod_id = vod_id
        if (len(vod_id) > 0):
            # Can play on-demand -> Add "Play:" before the title
            # and make it playable
            episode.IsPlayable = True
            episode.title = kodiutils.get_string(30070).format(title)
        else:
            episode.title = title

        episode.plot = '{0}\n\n{1}'.format(episode_name, row['description'])

        if (episode.IsPlayable):
            # Display the playable episode
            episodes.append((add_playable_episode_directory_item(episode)))
        else:
            # Simply display text
            episodes.append((None, episode.kodi_list_item, False))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    xbmcplugin.endOfDirectory(plugin.handle, succeeded=True, cacheToDisc=False)
    return (row_count)


#
# Video On Demand Mennu
#


@plugin.route('/vod/index')
def vod_index():
    xbmc.log('Creating Video On Demand Men')
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
        plugin.url_for(vod_episode_list, 'get_latest_episodes', 'None', 0,
                       xbmcplugin.SORT_METHOD_UNSORTED), li, True)
    # Most Watched
    li = xbmcgui.ListItem(kodiutils.get_string(30044))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list, 'get_most_watched_episodes', 'None',
                       0, xbmcplugin.SORT_METHOD_UNSORTED), li, True)
    # All
    li = xbmcgui.ListItem(kodiutils.get_string(30045))
    li.setArt(art)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list, 'get_all_episodes', 'None', 0,
                       xbmcplugin.SORT_METHOD_TITLE), li, True)

    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_WIDELIST,
                                              xbmcplugin.SORT_METHOD_NONE,
                                              'videos')

    return (True)


# By Program (Programs Tab on NHK World Site)
@plugin.route('/vod/programs/')
def vod_programs():
    """VOD Programs (Programs Tab on NHK World Site)
    Returns:
        [str] -- [Last program ID added]
    """
    program_json = utils.get_json(
        nhk_api.rest_url['get_programs'])['vod_programs']['programs']
    row_count = 0
    episodes = []

    for program_id in program_json:
        row = program_json[program_id]
        row_count = row_count + 1
        total_episodes = int(row['total_episode'])
        if total_episodes > 0:
            # Only show programs that have at lease on episode
            episode = Episode()
            episode.title = kodiutils.get_episodelist_title(
                row['title_clean'], total_episodes)
            episode.plot = row['description_clean']
            episode.thumb = row['image']
            episode.fanart = row['image_l']
            episode.video_info = kodiutils.get_1080_HD_video_info()

            # Create the directory item
            episodes.append(
                (plugin.url_for(vod_episode_list, 'get_programs_episode_list',
                                program_id, 1,
                                xbmcplugin.SORT_METHOD_UNSORTED),
                 episode.kodi_list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_TITLE,
                                              'seasons')

    # Return last valid program program Id - useful for debugging
    if (row_count > 0):
        return (program_id)
    else:
        return (None)


@plugin.route('/vod/categories/')
def vod_categories():
    """VOD Categories (Categories Tab on NHK World Site)
    Returns:
        [str] -- [Last category ID added]
    """
    api_result_json = utils.get_json(nhk_api.rest_url['get_categories'])
    row_count = 0
    episodes = []
    for row in api_result_json['vod_categories']:
        row_count = row_count + 1
        episode = Episode()

        episode.title = kodiutils.get_episodelist_title(
            row['name'], row['count'])
        episode.absolute_image_url = True
        episode.thumb = row['icon_l']
        episode.fanart = row['icon_l']
        episode.video_info = kodiutils.get_1080_HD_video_info()

        # Create the directory item
        category_id = row['category_id']
        episodes.append(
            (plugin.url_for(vod_episode_list, 'get_categories_episode_list',
                            category_id, 0, xbmcplugin.SORT_METHOD_UNSORTED),
             episode.kodi_list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_TITLE,
                                              'videos')

    # Return last valid category ID - useful for debugging
    if (row_count > 0):
        return (category_id)
    else:
        return (None)


@plugin.route('/vod/playlists/')
def vod_playlists():
    """VOD Playlists (Playlists Tab on NHK World Site)
    Returns:
        [str] -- [Last playlist ID added]
    """
    api_result_json = utils.get_json(nhk_api.rest_url['get_playlists'])
    row_count = 0
    episodes = []
    for row in api_result_json['data']['playlist']:
        row_count = row_count + 1

        episode = Episode()
        episode.title = kodiutils.get_episodelist_title(
            row['title_clean'], row['track_total'])
        episode.thumb = row['image_square']
        episode.fanart = row['image_square']

        playlist_id = row['playlist_id']
        episodes.append(
            (plugin.url_for(vod_episode_list, 'get_playlists_episode_list',
                            playlist_id, 0, xbmcplugin.SORT_METHOD_TITLE),
             episode.kodi_list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              xbmcplugin.SORT_METHOD_UNSORTED,
                                              'videos')

    # Return last valid playlist ID - useful for debugging
    if (row_count > 0):
        return (playlist_id)
    else:
        return (None)


def add_playable_episode_directory_item(episode, enforce_cache=False):
    """ Add a Kodi directory item for a playable episode """
    # If the vod_id is in cache and cache is being used,
    # diretly add the URL otherwise dynmaically resolve it
    # via play_vod_episode()
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
            m3u8_play_path = nhk_api.rest_url['episode-m3u_generator'].format(
                cached_episode['M3u8Path'])

            episode.url = m3u8_play_path
            episode.aspect = cached_episode['Aspect']
            episode.width = cached_episode['Width']
            episode.height = cached_episode['Height']
            episode.onair = cached_episode['OnAir']

            returnValue = [episode.url, episode.kodi_list_item, False]
            return (returnValue)

    # Not in cache - need to be resolve dynmaically
    play_url = plugin.url_for(play_vod_episode, episode.vod_id)
    xbmc.log('Dynamic Play URL: {0}'.format(play_url))
    returnValue = [play_url, episode.kodi_list_item, False]
    return (returnValue)


@plugin.route('/vod/episode_list/<api_method>/<id>/<show_only_subtitle>/' +
              '<sort_method>/')
def vod_episode_list(api_method,
                     id,
                     show_only_subtitle,
                     sort_method,
                     enforceCache=False):
    """[summary]
        Video On Demand - Episode List

        Creates a folded with list items based on the requested NHK API Method
        (e.g. Programs, Categories, etc.)
    Returns:
        [Episode] -- [Last Episode that was added]
    """
    # Only format api_url when a non-0 valze for id was provided
    # some APIs do not need an id
    if (id != 'None'):
        api_url = nhk_api.rest_url[api_method].format(id)
    else:
        api_url = nhk_api.rest_url[api_method]

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
    episodes = []
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
            episode.plot_include_broadcast_detail = True

        episode.plot = description

        # Add the current episode directory item
        episodes.append((add_playable_episode_directory_item(episode)))

    xbmcplugin.addDirectoryItems(plugin.handle, episodes, len(episodes))
    sort_method = int(sort_method)
    kodiutils.set_video_directory_information(plugin.handle,
                                              kodiutils.VIEW_MODE_INFOWALL,
                                              sort_method, 'videos')

    # Used for unit testing
    # only successfull hif we processed at least one episode
    if (row_count > 0):
        return (episode)
    else:
        return (None)


# Video On Demand - Play Episode
@plugin.route('/vod/play_episode/<vod_id>/')
def play_vod_episode(vod_id, disable_cache=False):

    if (disable_cache is True):
        # Overwrite use of backend
        use_backend = False
    else:
        use_backend = USE_CACHE

    xbmc.log('VOD_ID: {0}'.format(vod_id))
    xbmc.log('DISABLE CACHE: {0}'.format(disable_cache))
    xbmc.log('USE BACKEND: {0}'.format(use_backend))
    xbmc.log('PLUGIN HANDLE: {0}'.format(plugin.handle))

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

        # Use the M3U8 file that is generated by NHK
        # This file contains the videos in LQ, SD, 720P & 1080P
        # Kodi will select the best fid based on the
        # Internet Bandwidth Restriction Setting
        m3u8_play_path = nhk_api.rest_url['episode-m3u_generator'].format(
            cached_episode['M3u8Path'])
        episode.url = m3u8_play_path
        xbmc.log('Episode M3U8 URL:'.format(episode.url))
        episode.aspect = cached_episode['Aspect']
        episode.width = cached_episode['Width']
        episode.height = cached_episode['Height']
        if (cached_episode['OnAir'] is not None):
            episode.broadcast_start_date = cached_episode['OnAir']
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
        episode.plot = episode_detail['description_clean']
        episode.pgm_no = episode_detail['pgm_no']
        episode.duration = episode_detail['movie_duration']

        # Get episode URL and video information
        player_url = nhk_api.rest_url['video_url'].format(program_Uuid)
        assets_json = utils.get_json(
            player_url)['response']['WsProgramResponse']['program']['asset']

        # Collect all the information to create an M3U8 file
        m3u8_elements = []

        # Get the reference file (HD)
        reference_file_json = assets_json['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]

        hasReferenceFile = False
        # Only add the reference URL if exists (sometimes it doesn't!!)
        reference_url = nhk_api.rest_url['episode_url'].format(play_path)
        if (utils.check_url_exists(reference_url) is True):
            directory = reference_file_json['rtmp']['directory'] + '/'
            m3u8_path = play_path.replace(directory, '')
            bitrate = reference_file_json['videoBitrate']
            m3u8_element = '{0}:{1}'.format(bitrate, m3u8_path)
            episode.aspect = reference_file_json['aspectRatio']
            episode.width = reference_file_json['videoWidth']
            episode.height = reference_file_json['videoHeight']
            hasReferenceFile = True
            m3u8_elements.append(m3u8_element)

        # Loop through the assets
        index = 0
        for asset in assets_json['assetFiles']:
            directory = asset['rtmp']['directory'] + '/'
            play_path = asset['rtmp']['play_path'].split('?')[0]
            m3u8_path = play_path.replace(directory, '')
            bitrate = asset['videoBitrate']
            if (index == 0):
                # First Asset
                if (hasReferenceFile is False):
                    # No reference file, use first asset information
                    episode.aspect = asset['aspectRatio']
                    episode.width = asset['videoWidth']
                    episode.height = asset['videoHeight']
            m3u8_element = '{0}:{1}'.format(bitrate, m3u8_path)
            m3u8_elements.append(m3u8_element)
            index = index + 1

        # Create a valid m3U8 generator URL
        m3u8_delimiter = ','
        m3u8_media = m3u8_delimiter.join(m3u8_elements)
        m3u8_play_path = nhk_api.rest_url['episode-m3u_generator'].format(
            m3u8_media)
        episode.url = m3u8_play_path
        xbmc.log('Episode M3U8 URL: {0}'.format(episode.url))
        episode.aspect = reference_file_json['aspectRatio']
        episode.width = reference_file_json['videoWidth']
        episode.height = reference_file_json['videoHeight']

    xbmcplugin.setResolvedUrl(plugin.handle, True, episode.kodi_list_item)
    return (episode.url)


#  Play News or At A Glance Item
@plugin.route(
    '/news/play_news_item/<path:api_url>/<news_id>/<item_type>/<title>/')
def play_news_item(api_url, news_id, item_type, title):
    """ Play a news item
    can either be 'news' or 'ataglance'
    """
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
    else:
        return (False)

    xbmc.log('Play Path: {0}'.format(play_path))
    if (play_path is not None):
        episode = Episode()
        episode.vod_id = news_id
        episode.title = title
        episode.url = play_path
        episode.video_info = kodiutils.get_SD_video_info()
        episode.IsPlayable = True
        xbmcplugin.setResolvedUrl(plugin.handle, True, episode.kodi_list_item)
        return (True)
    else:
        # Couldn't find video
        xbmc.log('Couldnt find video {0}'.format(api_url))
        return (False)


#
# Main loop
#


def run():
    plugin.run()
