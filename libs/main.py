# Main Plug-in logic
import urllib
import urlparse
import re
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import os
import datetime
from libs import utils
from libs import nhk_api

# Define globale variables that will be later overridden at run-time
# Populate with default values to that we do unit-testing

LOGLEVEL = xbmc.LOGDEBUG
PLUGIN_ID = 'not_implemented_ye'
addon_handle = 0
base_url='http://not_implemented_yet'
nhk_icon="not_implemented_yet.png"

# Main Menu


def add_directory_main_menu():
    xbmc.log('Creating Main Menu', level=LOGLEVEL)
    add_directory_item('NHK World On Demand', '', 'add_directory_vod_menu', nhk_icon)
    add_live_stream()
    xbmcplugin.endOfDirectory(addon_handle)
    return (True)

# Video on Domand Menu


def add_directory_vod_menu():
    xbmc.log('Creating Video On Demand Menu', level=LOGLEVEL)
    add_directory_item('Programs', '', 'add_directory_vod_programs', nhk_icon)
    add_directory_item(
        'Latest Episodes', nhk_api.rest_url['get_latest_episodes'], 'add_directory_vod_episodelist', nhk_icon)
    add_directory_item('Categories', '', 'add_directory_vod_categories', nhk_icon)
    add_directory_item('Playlists', '', 'add_directory_vod_playlists', nhk_icon)
    add_directory_item(
        'Most Watched', nhk_api.rest_url['get_most_watched_episodes'], 'add_directory_vod_episodelist', nhk_icon)
    add_directory_item(
        'All Episodes', nhk_api.rest_url['get_all_episodes'], 'add_directory_vod_episodelist', nhk_icon)
    xbmcplugin.endOfDirectory(addon_handle)
    return(True)


# Create content list
def add_directory_item(name, url, mode, iconimage):
    plugin_url = utils.build_url(base_url,
                                 {'url': url, 'mode': mode})
    li = xbmcgui.ListItem(name)
    li.setArt({'thumb': iconimage, 'fanart': iconimage})
    xbmc.log(
        'Creating Directory Item {0} - {1}'.format(plugin_url, name.encode('ascii', 'ignore')), level=LOGLEVEL)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin_url,
                                listitem=li, isFolder=True)


# live streams
def add_live_stream():
    
    livestream_url = 'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_4M.m3u8'
    xbmc.log('1080p Livestream Akamai URL: {0}'.format(livestream_url), level=LOGLEVEL)
    title = 'NHK World Live Stream'
    poster_image = nhk_icon
    thumb_image = nhk_icon
    li = xbmcgui.ListItem(title)
    plot = title
    li.setArt({'thumb': thumb_image, 'poster': poster_image,
                'fanart': poster_image})
    video_info = {
        'aspect': '1.78',
        'width': '1920',
        'height': '1080'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'title': title, 'plot': plot})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=livestream_url,
                                listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)
    return(True)


#
# Video On Demand
#

# Video On Demand - By Program (Programs Tab on NHK World Site)
def add_directory_vod_programs():

    api_result_json = utils.get_json(nhk_api.rest_url['get_programs'])
    program_json = api_result_json['vod_programs']['programs']
    row_count = 0
    for row in program_json:
        row_count = +1
        series = program_json[row]['title_clean']
        plot = program_json[row]['description_clean']
        poster_image = utils.get_NHK_website_url(program_json[row]['image_l'])
        thumb_image = utils.get_NHK_website_url(program_json[row]['image'])
        total_episodes = program_json[row]['total_episode']
        if (total_episodes == 1):
            series = u'{0} - {1} episode'.format(series, total_episodes)
        else:
            series = u'{0} - {1} episodes'.format(series, total_episodes)
        detail_url = nhk_api.rest_url['get_programs_episode_list'].format(row)
        if(total_episodes > 0):
            plugin_url = utils.build_url(
                base_url, {'url': detail_url, 'mode': 'add_directory_vod_episodelist_onlySubtitle'})
            li = xbmcgui.ListItem(series)
            li.setArt({'thumb': thumb_image, 'poster': poster_image,
                       'fanart': poster_image})
            li.setInfo('video', {'mediatype': 'series',
                                 'title': series, 'plot': plot})
            xbmc.log('Creating Directory Item {0} - {1}'.format(
                plugin_url, series.encode('ascii', 'ignore')), level=LOGLEVEL)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin_url,
                                        listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.setContent(addon_handle, 'videos')
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(detail_url)
    else:
        return(None)

# Categories


def add_directory_vod_categories():

    api_result_json = utils.get_json(nhk_api.rest_url['get_categories'])
    row_count = 0
    for row in api_result_json['vod_categories']:
        row_count = +1
        categoryId = row['category_id']
        name = row['name']
        total_epsiodes = row['count']
        if (total_epsiodes == 1):
            name = u'{0} - {1} episode'.format(name, total_epsiodes)
        else:
            name = u'{0} - {1} episodes'.format(name, total_epsiodes)

        thumb_image = row['icon_l']
        detail_url = nhk_api.rest_url['get_categories_episode_list'].format(
            categoryId)
        if(total_epsiodes > 0):
            add_directory_item(
                name, detail_url, 'add_directory_vod_episodelist', thumb_image)

    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.setContent(addon_handle, 'videos')
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(detail_url)
    else:
        return(None)

# Playlists


def add_directory_vod_playlists():

    api_result_json = utils.get_json(nhk_api.rest_url['get_playlists'])
    row_count = 0
    for row in api_result_json['data']['playlist']:
        row_count = +1
        playlistId = row['playlist_id']
        name = row['title_clean']
        total_epsiodes = row['track_total']
        if (total_epsiodes == 1):
            name = u'{0} - {1} episode'.format(name.encode, total_epsiodes)
        else:
            name = u'{0} - {1} episodes'.format(name, total_epsiodes)

        thumb_image = utils.get_NHK_website_url(row['image_square'])
        detail_url = nhk_api.rest_url['get_playlists_episode_list'].format(
            playlistId)

        if(total_epsiodes > 0):
            add_directory_item(
                name, detail_url, 'add_directory_vod_playlist_episodes', thumb_image)

    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.setContent(addon_handle, 'videos')
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(detail_url)
    else:
        return(None)


# Video On Demand - Episode List
def add_directory_vod_episode_list(url, showOnlySubtitle, isFromPlaylist):
    xbmc.log('Displaying Episode List for URL: {0}'.format(
        url), level=LOGLEVEL)
    api_result_json = utils.get_json(url)
    if (isFromPlaylist):
        program_json = api_result_json['data']['playlist'][0]['track']
    else:
        program_json = api_result_json['data']['episodes']

    row_count = 0
    for row in program_json:
        row_count = +1
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if (showOnlySubtitle or len(title) == 0):
            episode = u'{0}'.format(subtitle)
        else:
            episode = u'{0} - {1}'.format(title, subtitle)

        if (len(title) == 0):
            fullEpisodeName = u'{0}'.format(subtitle)
        else:
            fullEpisodeName = u'{0} - {1}'.format(title, subtitle)

        plot = row['description_clean']
        largeImaga = utils.get_NHK_website_url(row['image_l'])
        thumb_image = utils.get_NHK_website_url(row['image'])
        promoImage = utils.get_NHK_website_url(row['image_promo'])
        vid_id = row['vod_id']
        pgm_id = row['pgm_id']
        pgm_no = row['pgm_no']
        duration = row['movie_duration']

        # Check if we have an aired date
        onair = row['onair']
        if (onair is not None):
            utc_time = datetime.datetime.utcfromtimestamp(onair/1000)
            plot = u'Aired: {0} ({1}-{2})\n\n{3}'.format(
                utc_time.strftime('%Y-%m-%d'), pgm_id, pgm_no, plot)
            year = int(utc_time.strftime('%Y'))
            dateadded = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            year = 0
            dateadded = ''
            pass

        plugin_url = utils.build_url(base_url, {'mode': 'add_directory_vod_single_epsiode', 'title': fullEpisodeName.encode('ascii', 'ignore'), 'vid_id': vid_id, 'plot': plot.encode(
            'ascii', 'ignore'), 'duration': duration, 'episode': pgm_no, 'year': year, 'dateadded': dateadded})
        li = xbmcgui.ListItem(episode)
        li.setArt(
            {'thumb': thumb_image, 'poster': promoImage, 'fanart': largeImaga})
        li.setInfo('video', {'mediatype': 'episode', 'title': fullEpisodeName, 'plot': plot,
                             'duration': duration, 'episode': pgm_no, 'year': year, 'dateadded': dateadded})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin_url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.setContent(addon_handle, 'videos')
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
    # Used for unit testing - only successfull if we processed at least one episode
    if (row_count > 0):
        return(vid_id)
    else:
        return(None)


# Video On Demand - Display Episode
def show_episode(title, vid_id, plot, duration, episode, year, dateadded):
    r = utils.get_url(
        'https://movie-s.nhk.or.jp/v/refid/nhkworld/prefid/{0}?embed=js&targetId=videoplayer&de-responsive=true&de-callback-method=nwCustomCallback&de-appid={1}&de-subtitle-on=false'.format(vid_id, vid_id))
    playerJS = r.text
    # Parse the output of the Player JS file for the UUID of the episode
    match = re.compile("'data-de-program-uuid','(.+?)'").findall(playerJS)
    if (match.count > 0):
        p_uuid = match[0].replace("['", "").replace("']", "")
        video_url = 'https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v={0}'.format(
            p_uuid)
        api_result_json = utils.get_json(video_url)
        vod_program = api_result_json['response']['WsProgramResponse']['program']
        reference_file_json = vod_program['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        episode_url = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/{0}/chunklist.m3u8'.format(
            play_path)
        xbmc.log('Episode Akamai URL: {0}'.format(episode_url), level=LOGLEVEL)
        poster_image = vod_program['posterUrl']
        thumb_image = vod_program['thumbnailUrl']
        li = xbmcgui.ListItem('Watch {0}'.format(title))
        li.setArt({'thumb': thumb_image, 'poster': poster_image,
                   'fanart': poster_image})
        video_info = {
            'aspect': reference_file_json['aspectRatio'],
            'width': reference_file_json['videoWidth'],
            'height': reference_file_json['videoHeight'],
        }
        li.addStreamInfo('video', video_info)
        li.setInfo('video', {'mediatype': 'episode', 'title': title, 'plot': plot,
                             'duration': duration, 'episode': episode, 'year': year, 'dateadded': dateadded})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=episode_url,
                                    listitem=li, isFolder=False)
        xbmcplugin.endOfDirectory(addon_handle)
        return(episode_url)
    else:
        xbmc.log('Could not retrieve Akamai URL for VID_ID {0}'.format(
            vid_id), level=xbmc.LOGFATAL)
        return (None)

# Main logic
# Called from default.py everytime the user selects and item in Kodi

def run(target_url, execution_mode, params):

    xbmc.log('Excution mode: {0}, Target Url: {1}, # of parameters {2}'.format(execution_mode, target_url, len(params)), level = LOGLEVEL)

    if execution_mode == None:
        add_directory_main_menu()

    elif execution_mode == 'add_directory_vod_menu':
        add_directory_vod_menu()

    elif execution_mode == 'add_directory_vod_episodelist':
        add_directory_vod_episode_list(target_url, False, False)

    elif execution_mode == 'add_directory_vod_programs':
        add_directory_vod_programs()

    elif execution_mode == 'add_directory_vod_categories':
        add_directory_vod_categories()

    elif execution_mode == 'add_directory_vod_playlists':
        add_directory_vod_playlists()

    elif execution_mode == 'add_directory_vod_episodelist_onlySubtitle':
        add_directory_vod_episode_list(target_url, True, False)

    elif execution_mode == 'add_directory_vod_playlist_episodes':
        add_directory_vod_episode_list(target_url, False, True)

    elif execution_mode == 'add_directory_vod_single_epsiode':
        show_episode(params.get('title', None)[0], params.get('vid_id', None)[0], params.get('plot', None)[0], params.get(
            'duration', None)[0], params.get('episode', None)[0], params.get('year', None)[0], params.get('dateadded', None)[0])
    else:
        xbmc.log('Couldnt find valid excution mode: {0}'.format(
            execution_mode), level=xbmc.LOGFATAL)
