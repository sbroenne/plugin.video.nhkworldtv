# -*- coding: utf-8 -*-

import random
import re
from datetime import datetime

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

import kodiutils
import nhk_api
import routing
import utils

# Initiate constants and plug-in
ADDON = xbmcaddon.Addon()
NHK_ICON = ADDON.getAddonInfo('icon')
NHK_FANART = ADDON.getAddonInfo('fanart')
plugin = routing.Plugin()

# View Modes from the default Estuary skin
VIEW_MODE_INFOWALL = 54
VIEW_MODE_WALL = 500
VIEW_MODE_WIDELIST = 55


# Start page of the plug-in
@plugin.route('/')
def index():
    xbmc.log('Creating Main Menu')

    # Add menus
    add_top_stories_menu_item()
    add_on_demand_menu_item()
    add_live_stream_menu_item()
    add_live_schedule_menu_item()

    # Set-up view
    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.endOfDirectory(plugin.handle)
    return (True)


#  Add the Top Stories menu
def add_top_stories_menu_item():
    xbmc.log('Adding top stories menu item')

    # Getting top story
    api_result_json = utils.get_json(nhk_api.rest_url['homepage_news'])
    featured_news = api_result_json['data'][0]

    thumbnails = featured_news['thumbnails']

    if (thumbnails is None):
        # Featured news does not have a thumbnail
        thumb_image = NHK_ICON
        fanart_image = NHK_FANART
    else:
        thumb_image = utils.get_NHK_website_url(
            featured_news['thumbnails']['small'])
        fanart_image = utils.get_NHK_website_url(
            featured_news['thumbnails']['middle'])

    pgm_title = featured_news['title']
    pgm_description = featured_news['description']
    title = kodiutils.get_string(30010)
    output = kodiutils.get_string(30012).format(pgm_title, pgm_description)

    li = xbmcgui.ListItem(title)
    li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
    video_info = kodiutils.get_SD_video_info()
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(top_stories_list), li, True)
    return (True)


# Add on-demand menu item
def add_on_demand_menu_item():

    xbmc.log('Adding on-demand menu item')
    # Getting random on-demand episode to show
    api_result_json = utils.get_json(nhk_api.rest_url['homepage_ondemand'])
    featured_episodes = api_result_json['data']['items']

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
        pgm_title = program_json['pgm_title']
        subtitle = program_json['subtitle']

    fanart_image = utils.get_NHK_website_url(program_json['image_pc'])
    thumb_image = utils.get_NHK_website_url(program_json['image_sp'])
    title = kodiutils.get_string(30020)
    episode_name = utils.get_episode_name(pgm_title, subtitle)

    output = kodiutils.get_string(30022).format(episode_name)
    li = xbmcgui.ListItem(title)
    li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
    video_info = kodiutils.get_1080_HD_video_info()
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_index), li,
                                True)
    return (True)


# Add live stream menu item
def add_live_stream_menu_item():
    xbmc.log('Adding live stream menu item')
    livestream_url = nhk_api.rest_url['live_stream_url']
    xbmc.log('1080p Livestream Akamai URL: {0}'.format(livestream_url))

    title = kodiutils.get_string(30030)
    li = xbmcgui.ListItem(title)

    xbmc.log('Retrieving live stream next shows')
    api_result_json = utils.get_json(nhk_api.rest_url['get_livestream'], False)
    program_json = api_result_json['channel']['item']

    # Currently playing
    row = program_json[0]

    # Schedule Information
    pubDate = int(row['pubDate']) / 1000
    endDate = int(row['endDate']) / 1000

    broadcast_start_local = utils.to_local_time(pubDate)
    broadcast_end_local = utils.to_local_time(endDate)

    # Live porgram
    fanart_image = utils.get_NHK_website_url(row['thumbnail'])
    thumb_image = utils.get_NHK_website_url(row['thumbnail_s'])

    # Title and Description
    full_title = u'{0}\n\n{1}'.format(row['title'], row['description'])
    plot = u'{0}-{1}: {2}'.format(broadcast_start_local.strftime('%H:%M'),
                                  broadcast_end_local.strftime('%H:%M'),
                                  full_title)

    li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
    video_info = kodiutils.get_1080_HD_video_info()
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': plot})
    xbmcplugin.addDirectoryItem(plugin.handle, livestream_url, li, False)
    return (True)


# Add live schedule menu item


def add_live_schedule_menu_item():
    xbmc.log('Adding live schedule menu item')

    title = kodiutils.get_string(30036)
    li = xbmcgui.ListItem(title)

    xbmc.log('Retrieving live stream next shows')
    api_result_json = utils.get_json(nhk_api.rest_url['get_livestream'], False)
    program_json = api_result_json['channel']['item']

    no_of_epsisodes = len(program_json)
    featured_episode = random.randint(1, no_of_epsisodes - 1)

    # Featured Episode
    row = program_json[featured_episode]

    # Schedule Information
    pubDate = int(row['pubDate']) / 1000
    endDate = int(row['endDate']) / 1000
    broadcast_start_local = utils.to_local_time(pubDate)
    broadcast_end_local = utils.to_local_time(endDate)
    fanart_image = utils.get_NHK_website_url(row['thumbnail'])
    thumb_image = utils.get_NHK_website_url(row['thumbnail_s'])

    title = u'{0}-{1}: {2}'.format(broadcast_start_local.strftime('%H:%M'),
                                   broadcast_end_local.strftime('%H:%M'),
                                   row['title'])
    output = '{0}\n\n{1}'.format(
        kodiutils.get_string(30022).format(title), row['description'])

    li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
    video_info = kodiutils.get_1080_HD_video_info()
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(live_schedule_index), li, True)
    return (True)


#
# Video On Demand Mennu
#


@plugin.route('/vod/index')
def vod_index():
    xbmc.log('Creating Video On Demand Menu')
    xbmcplugin.addDirectoryItem(
        plugin.handle, plugin.url_for(vod_programs),
        xbmcgui.ListItem(kodiutils.get_string(30040), iconImage=NHK_ICON),
        True)
    xbmcplugin.addDirectoryItem(
        plugin.handle, plugin.url_for(vod_categories),
        xbmcgui.ListItem(kodiutils.get_string(30041), iconImage=NHK_ICON),
        True)
    xbmcplugin.addDirectoryItem(
        plugin.handle, plugin.url_for(vod_playlists),
        xbmcgui.ListItem(kodiutils.get_string(30042), iconImage=NHK_ICON),
        True)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list,
                       nhk_api.rest_url['get_latest_episodes'], 0, 0,
                       xbmcplugin.SORT_METHOD_DATEADDED),
        xbmcgui.ListItem(kodiutils.get_string(30043), iconImage=NHK_ICON),
        True)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list,
                       nhk_api.rest_url['get_most_watched_episodes'], 0, 0,
                       xbmcplugin.SORT_METHOD_NONE),
        xbmcgui.ListItem(kodiutils.get_string(30044), iconImage=NHK_ICON),
        True)
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(vod_episode_list, nhk_api.rest_url['get_all_episodes'],
                       0, 0, xbmcplugin.SORT_METHOD_TITLE),
        xbmcgui.ListItem(kodiutils.get_string(30045), iconImage=NHK_ICON),
        True)
    kodiutils.set_view_mode(VIEW_MODE_WIDELIST)
    xbmcplugin.endOfDirectory(plugin.handle)
    return (True)


# By Program (Programs Tab on NHK World Site)
@plugin.route('/vod/programs/')
def vod_programs():

    api_result_json = utils.get_json(nhk_api.rest_url['get_programs'])
    program_json = api_result_json['vod_programs']['programs']
    row_count = 0
    for row in program_json:
        row_count = row_count + 1
        title = program_json[row]['title_clean']
        plot = program_json[row]['description_clean']
        poster_image = utils.get_NHK_website_url(program_json[row]['image_l'])
        thumb_image = utils.get_NHK_website_url(program_json[row]['image'])
        total_episodes = program_json[row]['total_episode']
        if (total_episodes == 1):
            title = u'{0} - {1} episode'.format(title, total_episodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_episodes)
        api_url = nhk_api.rest_url['get_programs_episode_list'].format(row)
        if (total_episodes > 0):
            li = xbmcgui.ListItem(title)
            li.setArt({
                'thumb': thumb_image,
                'poster': poster_image,
                'fanart': poster_image
            })
            li.setInfo('video', {
                'mediatype': 'videos',
                'title': title,
                'plot': plot
            })
            xbmc.log('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(vod_episode_list, api_url, 1, 0,
                               xbmcplugin.SORT_METHOD_TITLE), li, True)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)
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
        categoryId = row['category_id']
        title = row['name']
        total_epsiodes = row['count']
        if (total_epsiodes == 1):
            title = u'{0} - {1} episode'.format(title, total_epsiodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_epsiodes)

        thumb_image = row['icon_l']
        api_url = nhk_api.rest_url['get_categories_episode_list'].format(
            categoryId)
        if (total_epsiodes > 0):
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos', 'title': title})
            xbmc.log('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))
            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(vod_episode_list, api_url, 0, 0,
                               xbmcplugin.SORT_METHOD_TITLE), li, True)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_WALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)
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
        playlistId = row['playlist_id']
        title = row['title_clean']
        total_epsiodes = row['track_total']
        if (total_epsiodes == 1):
            title = u'{0} - {1} episode'.format(title, total_epsiodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_epsiodes)

        thumb_image = utils.get_NHK_website_url(row['image_square'])
        api_url = nhk_api.rest_url['get_playlists_episode_list'].format(
            playlistId)

        if (total_epsiodes > 0):
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos', 'title': title})
            xbmc.log('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(vod_episode_list, api_url, 0, 1,
                               xbmcplugin.SORT_METHOD_TITLE), li, True)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_WALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return (api_url)
    else:
        return (None)


# Video On Demand - Episode List
@plugin.route(
    '/vod/episode_list/<path:api_url>/<show_only_subtitle>/<is_from_playlist>/<sort_method>/'
)
def vod_episode_list(api_url, show_only_subtitle, is_from_playlist,
                     sort_method):
    xbmc.log('Displaying Episode List for URL: {0} - {1} - {2}'.format(
        api_url, show_only_subtitle, is_from_playlist))
    api_result_json = utils.get_json(api_url)
    if (int(is_from_playlist) == 1):
        program_json = api_result_json['data']['playlist'][0]['track']
    else:
        program_json = api_result_json['data']['episodes']

    row_count = 0
    for row in program_json:
        row_count = row_count + 1
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if int(show_only_subtitle) == 1:
            # Use the subtitle as the episode name
            episode_name = subtitle
        else:
            episode_name = utils.get_episode_name(title, subtitle)

        description = row['description_clean']
        largeImage = utils.get_NHK_website_url(row['image_l'])
        thumb_image = utils.get_NHK_website_url(row['image'])
        vod_id = row['vod_id']
        pgm_no = row['pgm_no']
        #pgm_id = row['pgm_id']
        duration = row['movie_duration']

        # Check if we have an aired date
        broadcast_start_timestamp = row['onair']
        broadcast_end_timestamp = row['vod_to']

        if (broadcast_start_timestamp is not None):
            broadcast_start_timestamp = int(broadcast_start_timestamp) / 1000
            broadcast_end_timestamp = int(broadcast_end_timestamp) / 1000

            # Convert to local time
            broadcast_start_local = utils.to_local_time(
                broadcast_start_timestamp)
            broadcast_end_local = utils.to_local_time(broadcast_end_timestamp)

            plot = kodiutils.get_string(30050).format(
                broadcast_start_local.strftime('%Y-%m-%d'),
                broadcast_end_local.strftime('%Y-%m-%d'), description)
            year = int(broadcast_start_local.strftime('%Y'))
            date_added_info_label = broadcast_start_local.strftime(
                '%Y-%m-%d %H:%M:%S')
        else:
            year = 0
            date_added_info_label = ''
            plot = description

        li = xbmcgui.ListItem(episode_name)
        li.setArt({'thumb': thumb_image, 'fanart': largeImage})
        li.setInfo(
            'video', {
                'mediatype': 'episode',
                'plot': plot,
                'duration': duration,
                'episode': pgm_no,
                'year': year,
                'dateadded': date_added_info_label
            })
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(show_episode,
                           vod_id=vod_id,
                           year=year,
                           dateadded=date_added_info_label), li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    sort_method = int(sort_method)
    xbmcplugin.addSortMethod(plugin.handle, sort_method)

    # If we sort by date added, make sure sort direction
    # is descending (e.g. for latest episodes)
    if (sort_method == xbmcplugin.SORT_METHOD_DATEADDED):
        kodiutils.set_sort_direction('Descending')

    xbmcplugin.endOfDirectory(plugin.handle)

    # Used for unit testing
    # only successfull if we processed at least one episode
    if (row_count > 0):
        return (vod_id)
    else:
        return (None)


# Video On Demand - Display Episode
@plugin.route('/vod/show_episode/<vod_id>/<year>/<dateadded>/')
def show_episode(vod_id, year, dateadded, enforceCache=False):

    if (enforceCache):
        use_backend = True
    else:
        use_backend = kodiutils.get_setting_as_bool('use_backend')

    if (use_backend):
        # Use NHK World TV Cloud Service to speed-up start of episode playback
        # The service runs on Azure in West Europe but should still speed up the lookup process dramatically since it uses a pre-loaded cache
        xbmc.log('Using Cloud Service to retrieve vod_id: {0}'.format(vod_id))
        program_json = utils.get_json(
            nhk_api.rest_url['nhkworldtv-backend'].format(vod_id))
        program_Uuid = program_json["ProgramUuid"]
        title = program_json['Title']
        plot = program_json['Plot']
        pgm_no = program_json['PgmNo']
        duration = program_json['Duration']
        play_path = program_json['PlayPath']
        aspect = program_json['Aspect']
        width = program_json['Width']
        height = program_json['Height']
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
        episode_json = utils.get_json(
            nhk_api.rest_url['get_episode_detail'].format(vod_id))
        episode_detail = episode_json['data']['episodes'][0]
        title = episode_detail['title_clean']
        plot = episode_detail['description_clean']
        pgm_no = episode_detail['pgm_no']
        duration = episode_detail['movie_duration']
        
        # Get episode URL and video information
        video_url = nhk_api.rest_url['video_url'].format(program_Uuid)
        api_result_json = utils.get_json(video_url)
        reference_file_json = api_result_json['response']['WsProgramResponse']['program']['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        aspect = reference_file_json['aspectRatio'],
        width = reference_file_json['videoWidth'],
        height = reference_file_json['videoHeight'],

    episode_url = nhk_api.rest_url['episode_url'].format(play_path)
    xbmc.log('Episode Akamai URL: {0}'.format(episode_url))
    li = xbmcgui.ListItem(path=episode_url)
    video_info = {
        'aspect': aspect,
        'width': width,
        'height': height,
    }
    li.addStreamInfo('video', video_info)
    li.setInfo(
        'video', {
            'mediatype': 'episode',
            'title': title,
            'plot': plot,
            'duration': duration,
            'episode': pgm_no,
            'year': year,
            'dateadded': dateadded
        })

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)
    return (episode_url)


# Top Stories - List
@plugin.route('/vod/top_stories_list/')
def top_stories_list():
    xbmc.log('Displaying Top Stories list')
    api_result_json = utils.get_json(nhk_api.rest_url['homepage_news'])
    MAX_ROW_COUNT = 12
    result_row_count = len(api_result_json['data'])
    # Only display MAX ROWS
    if (result_row_count < MAX_ROW_COUNT):
        MAX_ROW_COUNT = result_row_count

    for row_count in range(0, MAX_ROW_COUNT - 1):
        row = api_result_json['data'][row_count]
        title = row['title']
        description = row['description']
        thumbnails = row['thumbnails']

        if (thumbnails is None):
            # Featured news does not have a thumbnail
            thumb_image = NHK_ICON
            fanart_image = NHK_FANART
        else:
            thumb_image = utils.get_NHK_website_url(row['thumbnails']['small'])
            fanart_image = utils.get_NHK_website_url(
                row['thumbnails']['middle'])

        updated_at = int(row['updated_at']) / 1000
        updated_at_local = utils.to_local_time(updated_at)
        date_added_info_label = updated_at_local.strftime('%Y-%m-%d %H:%M:%S')
        year = int(updated_at_local.strftime('%Y'))

        time_difference_hours = datetime.now().hour - updated_at_local.hour
        if (time_difference_hours <= 1):
            time_difference = kodiutils.get_string(30060).format(
                time_difference_hours)
        else:
            time_difference = kodiutils.get_string(30061).format(
                time_difference_hours)
        plot = u'{0}\n\n{1}'.format(time_difference, description)

        if row['videos'] is not None:
            # Top stories that have a video attached to them
            title = kodiutils.get_string(30070).format(title)
            vod_id = row['id']
            video_xml_url = nhk_api.rest_url['get_news_xml'].format(vod_id)
            video_response = utils.get_url(video_xml_url)
            video_xml = str(video_response.content)
            start_pos = video_xml.find(vod_id)
            end_pos = video_xml.find('HQ')
            video_file = video_xml[start_pos:end_pos]
            video_url = nhk_api.rest_url['news_url'].format(video_file)
            duration = row['videos']['duration']
            minutes = int(duration / 60)
            seconds = duration - (minutes * 60)
            duration_text = '{0}m {1}s'.format(minutes, seconds)
            plot = u'{0} | {1}\n\n{2}'.format(duration_text, time_difference,
                                              description)

            li = xbmcgui.ListItem(path=video_url)
            li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
            video_info = kodiutils.get_SD_video_info()
            li.addStreamInfo('video', video_info)
            li.setInfo(
                'video', {
                    'mediatype': 'episode',
                    'title': title,
                    'plot': plot,
                    'duration': duration,
                    'year': year,
                    'dateadded': date_added_info_label
                })
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(plugin.handle, video_url, li, False)

        else:
            # No video attached to it
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
            li.setInfo(
                'video', {
                    'mediatype': 'episode',
                    'plot': plot,
                    'year': year,
                    'dateadded': date_added_info_label
                })
            xbmcplugin.addDirectoryItem(plugin.handle, None, li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_DATEADDED)
    kodiutils.set_sort_direction('Descending')
    xbmcplugin.endOfDirectory(plugin.handle)

    # Used for unit testing
    # only successfull if we processed at least top story
    if (row_count > 0):
        return (row_count)
    else:
        return (0)


#
# Live Schedule Menu
#


@plugin.route('/live_schedule/index')
def live_schedule_index():
    xbmc.log('Adding live schedule menu item')

    xbmc.log('Retrieving live stream next shows')
    api_result_json = utils.get_json(nhk_api.rest_url['get_livestream'], False)
    program_json = api_result_json['channel']['item']

    row_count = 0
    for row in program_json:
        row_count = row_count + 1

        # Schedule Information
        pubDate = int(row['pubDate']) / 1000
        endDate = int(row['endDate']) / 1000
        broadcast_start_local = utils.to_local_time(pubDate)
        broadcast_end_local = utils.to_local_time(endDate)

        # Live program
        fanart_image = utils.get_NHK_website_url(row['thumbnail'])
        thumb_image = utils.get_NHK_website_url(row['thumbnail_s'])

        # Title and Description
        title = row['title']
        subtitle = row['subtitle']
        description = row['description']

        vod_id = row['vod_id']
        playable = False
        if (len(vod_id) > 0):
            # Can play on-demand
            playable = True

        episode_name = utils.get_episode_name(title, subtitle)

        if (playable):
            title = kodiutils.get_string(30070).format(episode_name)
        else:
            title = u'{0}-{1}: {2}'.format(
                broadcast_start_local.strftime('%H:%M'),
                broadcast_end_local.strftime('%H:%M'), episode_name)

        plot = u'{0}\n\n{1}'.format(episode_name, description)
        year = int(broadcast_start_local.strftime('%Y'))
        date_added_info_label = broadcast_start_local.strftime(
            '%Y-%m-%d %H:%M:%S')

        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
        li.setInfo(
            'video', {
                'mediatype': 'episode',
                'plot': plot,
                'year': year,
                'dateadded': date_added_info_label
            })

        vod_id = row['vod_id']
        if (playable):
            # There is a video to play
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(
                plugin.handle,
                plugin.url_for(show_episode,
                               vod_id=vod_id,
                               year=year,
                               dateadded=date_added_info_label), li, False)
        else:
            xbmcplugin.addDirectoryItem(plugin.handle, None, li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_WIDELIST)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_DATEADDED)

    xbmcplugin.endOfDirectory(plugin.handle)

    if (row_count > 0):
        return (True)
    else:
        return (None)


def run():
    plugin.run()
