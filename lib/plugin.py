# -*- coding: utf-8 -*-

import random
import re
from datetime import datetime, timedelta

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
ADDON = xbmcaddon.Addon()
NHK_ICON = ADDON.getAddonInfo('icon')
NHK_FANART = ADDON.getAddonInfo('fanart')
plugin = routing.Plugin()

# View Modes from the default Estuary skin
VIEW_MODE_INFOWALL = 54
VIEW_MODE_WALL = 500
VIEW_MODE_WIDELIST = 55

#
# Helpers
#

#  Add the Top Stories menu
def get_episode_cache():
    # Use NHK World TV Cloud Service to speed-up episode URLlookup
    # The service runs on Azure in West Europe but should still speed up the lookup process dramatically since it uses a pre-loaded cache
    xbmc.log('Getting vod_id/video cache from Azure')

    max_episodes = 2000

    # Getting top story
    episodes = utils.get_json(cache_api.url['cache_get_program_list'].format(max_episodes))
    return (episodes)

# Episode Cache
EPISODE_CACHE = get_episode_cache()

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
    featured_news = utils.get_json(nhk_api.rest_url['homepage_news'])['data'][0]
    thumbnails = featured_news['thumbnails']

    episode = Episode()
    if (thumbnails is None):
        # Featured news does not have a thumbnail
        episode.thumb = NHK_ICON
        episode.fanart = NHK_FANART
    else:
        episode.thumb = featured_news['thumbnails']['small']
        episode.fanart = featured_news['thumbnails']['middle']
    
    episode.title = kodiutils.get_string(30010)
  
    # Create the plot field
    episode.plot = kodiutils.get_string(30012).format(featured_news['title'], featured_news['description'])
    
    # Create the directory itemn
    episode.video_info = kodiutils.get_SD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(top_stories_list), episode.kodi_list_item, True)
    return (True)


# Add on-demand menu item
def add_on_demand_menu_item():

    xbmc.log('Adding on-demand menu item')
    # Getting random on-demand episode to show
    featured_episodes = utils.get_json(nhk_api.rest_url['homepage_ondemand'])['data']['items']
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
    episode.plot = kodiutils.get_string(30022).format(utils.get_episode_name(pgm_title, program_json['subtitle']))
    episode.thumb = program_json['image_sp']
    episode.fanart = program_json['image_pc']

    # Create the directory itemn
    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(vod_index), episode.kodi_list_item, True)
    return (True)


# Add live stream menu item
def add_live_stream_menu_item():
    xbmc.log('Adding live stream menu item')
    xbmc.log('Retrieving live stream next shows')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'], False)['channel']['item']
 
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
    episode.url=nhk_api.rest_url['live_stream_url']
   
    # Title and Description
    full_title = u'{0}\n\n{1}'.format(row['title'], row['description'])
    episode.plot = u'{0}-{1}: {2}'.format(episode.broadcast_start_date.strftime('%H:%M'),
                                  episode.broadcast_end_date.strftime('%H:%M'),
                                  full_title)

    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle, episode.url, episode.kodi_list_item, False)
    return (True)


# Add live schedule menu item


def add_live_schedule_menu_item():
    xbmc.log('Adding live schedule menu item')

    xbmc.log('Retrieving live stream next shows')
    program_json = utils.get_json(nhk_api.rest_url['get_livestream'], False)['channel']['item']
    no_of_epsisodes = len(program_json)
    featured_episode = random.randint(1, no_of_epsisodes - 1)

    # Add live-schedule text
    episode = Episode()
    episode.title = kodiutils.get_string(30036)
  
    # Featured Episode
    row = program_json[featured_episode]

    # Schedule Information
    episode.broadcast_start_date = row['pubDate']
    episode.broadcast_end_date = row['endDate']
    episode.thumb = row['thumbnail_s']
    episode.fanart = row['thumbnail']

    title = u'{0}-{1}: {2}'.format(episode.broadcast_start_date.strftime('%H:%M'),
                                   episode.broadcast_end_date.strftime('%H:%M'),
                                   row['title'])
    episode.plot = '{0}\n\n{1}'.format(
        kodiutils.get_string(30022).format(title), row['description'])

    episode.video_info = kodiutils.get_1080_HD_video_info()
    xbmcplugin.addDirectoryItem(plugin.handle,
                                plugin.url_for(live_schedule_index), episode.kodi_list_item, True)
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
                       xbmcplugin.SORT_METHOD_DATE),
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

    program_json = utils.get_json(nhk_api.rest_url['get_programs'])['vod_programs']['programs']
    row_count = 0
  
    for row in program_json:
        row_count = row_count + 1
        episode = Episode()
        # Format title
        title = program_json[row]['title_clean']
        total_episodes = program_json[row]['total_episode']
        episodelist_title = utils.get_episodelist_title(title, total_episodes)
        episode.title = episodelist_title
        
        episode.plot = program_json[row]['description_clean']
        episode.thumb = utils.get_NHK_website_url(program_json[row]['image'])
        episode.fanart = utils.get_NHK_website_url(program_json[row]['image_l'])

        # Create the directory item
        api_url = nhk_api.rest_url['get_programs_episode_list'].format(row)
        xbmc.log('Creating Directory Item {0} - {1}'.format(
            api_url, title.encode('ascii', 'ignore')))

        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(vod_episode_list, api_url, 1, 0,
                            xbmcplugin.SORT_METHOD_DATE), episode.kodi_list_item, True)

    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_INFOWALL, xbmcplugin.SORT_METHOD_TITLE)
   
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
        # Format title
        title = row['name']
        total_epsiodes = row['count']
        episodelist_title = utils.get_episodelist_title(title, total_epsiodes)
        episode.title = episodelist_title

        episode.thumb = row['icon_l']
        episode.fanart = row['icon_l']
    
        # Create the directory item
        categoryId = row['category_id']
        api_url = nhk_api.rest_url['get_categories_episode_list'].format(
            categoryId)
        xbmc.log('Creating Directory Item {0} - {1}'.format(
            api_url, title.encode('ascii', 'ignore')))
        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(vod_episode_list, api_url, 0, 0,
                            xbmcplugin.SORT_METHOD_TITLE), episode.kodi_list_item, True)
    
    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_WALL, xbmcplugin.SORT_METHOD_TITLE)
  
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
        # Format title
        title = row['title_clean']
        total_epsiodes = row['track_total']
        episodelist_title = utils.get_episodelist_title(title, total_epsiodes)
        episode.title = episodelist_title
  
        episode.thumb = row['image_square']
        episode.fanart = row['image_square']
        
        playlistId = row['playlist_id']
        api_url = nhk_api.rest_url['get_playlists_episode_list'].format(
            playlistId)

        xbmc.log('Creating Directory Item {0} - {1}'.format(
            api_url, title.encode('ascii', 'ignore')))

        xbmcplugin.addDirectoryItem(
            plugin.handle,
            plugin.url_for(vod_episode_list, api_url, 0, 1,
                            xbmcplugin.SORT_METHOD_TITLE), episode.kodi_list_item, True)

    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_WALL, xbmcplugin.SORT_METHOD_TITLE)
    
    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return (api_url)
    else:
        return (None)


#
# Add a Kodi directory item for a playable episode
# If the vod_id is in cache and cache is being used, diretly add the URL otherwise dynmaically resolve it
# via show_epsisode()
#

def add_episode_directory_item(vod_id, episode_name, plot, duration, pgm_no, sort_date, year, thumb_image, large_image,enforce_cache = False):
    # Use the cache backend or not
    if (enforce_cache):
        use_backend = True
    else:
        use_backend = kodiutils.get_setting_as_bool('use_backend')

    if (use_backend):
        if (vod_id in EPISODE_CACHE):
            episode = EPISODE_CACHE[vod_id]
            # In cache - display directly
            play_path = episode["PlayPath"]
            aspect = episode['Aspect']
            width = episode['Width']
            height = episode['Height']
            episode_url = nhk_api.rest_url['episode_url'].format(play_path)
            xbmc.log('Episode Akamai URL: {0}'.format(episode_url))
            li = xbmcgui.ListItem(path=episode_url)
            li.setArt({'thumb': thumb_image, 'fanart': large_image})
            li.setInfo(
                'video', {
                    'mediatype': 'episode',
                    'title': episode_name,
                    'plot': plot,
                    'duration': duration,
                    'episode': pgm_no,
                    'year': year,
                    'date': sort_date
                })
            li.setProperty('IsPlayable', 'true')
        
            video_info = {
                'aspect': aspect,
                'width': width,
                'height': height,
            }
            li.addStreamInfo('video', video_info)
            xbmcplugin.addDirectoryItem(plugin.handle, episode_url, li)
            return(True)

    # Resolve URL dynamically
    li = xbmcgui.ListItem(episode_name)
    li.setArt({'thumb': thumb_image, 'fanart': large_image})
    li.setInfo(
        'video', {
            'mediatype': 'episode',
            'plot': plot,
            'duration': duration,
            'episode': pgm_no,
            'year': year,
            'date': sort_date
        })
    li.setProperty('IsPlayable', 'true')
    
    xbmcplugin.addDirectoryItem(
        plugin.handle,
        plugin.url_for(show_episode,
                    vod_id=vod_id,
                    year=year,
                    dateadded=sort_date), li, False)
    return(True)


# Video On Demand - Episode List
@plugin.route(
    '/vod/episode_list/<path:api_url>/<show_only_subtitle>/<is_from_playlist>/<sort_method>/'
)
def vod_episode_list(api_url, show_only_subtitle, is_from_playlist,
                     sort_method, enforceCache=False):
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
        episode = Episode()
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if int(show_only_subtitle) == 1:
            # Use the subtitle as the episode name
            episode_name = subtitle
        else:
            episode_name = utils.get_episode_name(title, subtitle)

        episode.title=episode_name
        description = row['description_clean']
        episode.thumb = row['image']
        episode.fanart = row['image_l']
        episode.vod_id = row['vod_id']
        episode.pgm_no = row['pgm_no']
        #pgm_id = row['pgm_id']
        episode.duration = row['movie_duration']

        # Check if we have an aired date
        broadcast_start_timestamp = row['onair']
     
        if (broadcast_start_timestamp is not None):
            episode.broadcast_start_date = broadcast_start_timestamp
            episode.broadcast_end_date = row['vod_to']


            episode.plot = kodiutils.get_string(30050).format(episode.broadcast_start_date.strftime('%Y-%m-%d'), episode.broadcast_end_date.strftime('%Y-%m-%d'), description)
            year = int(episode.broadcast_start_date.strftime('%Y'))
            sort_date =utils.get_sort_date(episode.broadcast_start_date)
        else:
            year = 0
            sort_date=""
            episode.plot = description
    
        # Add the current episode directory item
        add_episode_directory_item(episode.vod_id, episode.title, episode.plot, episode.duration, episode.pgm_no, sort_date, year, episode.thumb, episode.fanart, enforceCache)   

    sort_method = int(sort_method)
    kodiutils.set_video_directory_information(plugin.handle, VIEW_MODE_INFOWALL, sort_method)

    # Used for unit testing
    # only successfull if we processed at least one episode
    if (row_count > 0):
        return (episode.vod_id)
    else:
        return (None)


# Video On Demand - Display Episode
@plugin.route('/vod/show_episode/<vod_id>/<year>/<dateadded>/')
def show_episode(vod_id, year, dateadded, enforce_cache=False):

    if (enforce_cache):
        use_backend = True
    else:
        use_backend = kodiutils.get_setting_as_bool('use_backend')

    if (use_backend):
        # Use NHK World TV Cloud Service to speed-up start of episode playback
        # The service runs on Azure in West Europe but should still speed up the lookup process dramatically since it uses a pre-loaded cache
        xbmc.log('Using Cloud Service to retrieve vod_id: {0}'.format(vod_id))
        program_json = utils.get_json(
            cache_api.url['cache_get_program'].format(vod_id))
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
            'date': dateadded
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
        sort_date = utils.get_sort_date(updated_at_local)
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
                    'date': sort_date
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
                    'date': sort_date
                })
            xbmcplugin.addDirectoryItem(plugin.handle, None, li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_DATE)
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

        duration_diff = broadcast_end_local-broadcast_start_local
        duration = duration_diff.seconds
        
        # Live program
        large_image = utils.get_NHK_website_url(row['thumbnail'])
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
        sort_date = utils.get_sort_date(broadcast_start_local)

        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': thumb_image, 'fanart': large_image})
        li.setInfo(
            'video', {
                'mediatype': 'episode',
                'plot': plot,
                'year': year,
                'date': sort_date
            })

        vod_id = row['vod_id']
        if (playable):
            # Add the episode directory item
            add_episode_directory_item(vod_id, title, plot, duration, 0, sort_date, year, thumb_image, large_image)   
        else:
            xbmcplugin.addDirectoryItem(plugin.handle, None, li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    kodiutils.set_view_mode(VIEW_MODE_WIDELIST)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_DATE)

    xbmcplugin.endOfDirectory(plugin.handle)

    if (row_count > 0):
        return (True)
    else:
        return (None)

def run():
    plugin.run()
