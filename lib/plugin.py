# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
import kodiutils
import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent, addSortMethod, SORT_METHOD_TITLE, setResolvedUrl
from utils import get_json, get_NHK_website_url, get_url
from nhk_api import *
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from tzlocal import get_localzone
import re


ADDON = xbmcaddon.Addon()
nhk_icon = ADDON.getAddonInfo('icon')  # icon.png in addon directory
fanart_image = ADDON.getAddonInfo('fanart')  # icon.png in addon directory
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


@plugin.route('/')
def index():
    logger.debug('Creating Main Menu')
    title = 'NHK World On Demand'
    plot = 'Watch NHK World On Demand'
    li = ListItem(title)
    li.setArt({'thumb': nhk_icon,
               'fanart': fanart_image})
    video_info = {
        'aspect': '1.78',
        'width': '1920',
        'height': '1080'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': plot})
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_index), li, True)
    add_live_stream()
    endOfDirectory(plugin.handle)
    return (True)

# Add live stream URL


def add_live_stream():

    livestream_url = rest_url['live_stream_url']
    logger.debug('1080p Livestream Akamai URL: {0}'.format(livestream_url))
    title = 'NHK World Live Stream'
    li = ListItem(title)
    plot = 'Watch NHK World Live Stream'
    li.setArt({'thumb': nhk_icon,
               'fanart': fanart_image})
    video_info = {
        'aspect': '1.78',
        'width': '1920',
        'height': '1080'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': plot})
    addDirectoryItem(handle=plugin.handle, url=livestream_url,
                     listitem=li, isFolder=False)
    return(True)


#
# Video On Demand
#

@plugin.route('/vod/index')
def vod_index():
    logger.debug('Creating Video On Demand Menu')
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_programs), ListItem("Programs", iconImage=nhk_icon), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_categories), ListItem("Categories", iconImage=nhk_icon), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_playlists), ListItem("Playlists", iconImage=nhk_icon), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_latest_episodes'], 0, 0), ListItem("Latest Episodes", iconImage=nhk_icon), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_most_watched_episodes'],0, 0), ListItem("Most Watched", iconImage=nhk_icon), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_all_episodes'], 0, 0), ListItem("All Episodes", iconImage=nhk_icon), True)
    endOfDirectory(plugin.handle)
    return(True)



# By Program (Programs Tab on NHK World Site)
@plugin.route('/vod/programs/')
def vod_programs():

    api_result_json = get_json(rest_url['get_programs'])
    program_json = api_result_json['vod_programs']['programs']
    row_count = 0
    for row in program_json:
        row_count = +1
        title = program_json[row]['title_clean']
        plot = program_json[row]['description_clean']
        poster_image = get_NHK_website_url(program_json[row]['image_l'])
        thumb_image = get_NHK_website_url(program_json[row]['image'])
        total_episodes = program_json[row]['total_episode']
        if (total_episodes == 1):
            title = u'{0} - {1} episode'.format(title, total_episodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_episodes)
        api_url = rest_url['get_programs_episode_list'].format(row)
        if(total_episodes > 0):
            li = ListItem(title)
            li.setArt({'thumb': thumb_image, 'poster': poster_image,
                       'fanart': poster_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title, 'plot': plot})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 1, 0), li, True)

    endOfDirectory(plugin.handle)
    setContent(plugin.handle, 'videos')
    addSortMethod(plugin.handle, SORT_METHOD_TITLE)
    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(api_url)
    else:
        return(None)


# Categories

@plugin.route('/vod/categories/')
def vod_categories():

    api_result_json = get_json(rest_url['get_categories'])
    row_count = 0
    for row in api_result_json['vod_categories']:
        row_count = +1
        categoryId = row['category_id']
        title = row['name']
        total_epsiodes = row['count']
        if (total_epsiodes == 1):
            title = u'{0} - {1} episode'.format(title, total_epsiodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_epsiodes)

        thumb_image = row['icon_l']
        api_url = rest_url['get_categories_episode_list'].format(
            categoryId)
        if(total_epsiodes > 0):
            li = ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))
            addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 0, 0), li, True)

    endOfDirectory(plugin.handle)
    setContent(plugin.handle, 'videos')
    addSortMethod(plugin.handle, SORT_METHOD_TITLE)
    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(api_url)
    else:
        return(None)

# Playlists


@plugin.route('/vod/playlists/')
def vod_playlists():

    api_result_json = get_json(rest_url['get_playlists'])
    row_count = 0
    for row in api_result_json['data']['playlist']:
        row_count = +1
        playlistId = row['playlist_id']
        title = row['title_clean']
        total_epsiodes = row['track_total']
        if (total_epsiodes == 1):
            title = u'{0} - {1} episode'.format(title, total_epsiodes)
        else:
            title = u'{0} - {1} episodes'.format(title, total_epsiodes)

        thumb_image = get_NHK_website_url(row['image_square'])
        api_url = rest_url['get_playlists_episode_list'].format(
            playlistId)

        if(total_epsiodes > 0):
            li = ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 0, 1), li, True)
    endOfDirectory(plugin.handle)
    setContent(plugin.handle, 'videos')
    addSortMethod(plugin.handle, SORT_METHOD_TITLE)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(api_url)
    else:
        return(None)


# Video On Demand - Episode List
@plugin.route('/vod/episode_list/<path:api_url>/<show_only_subtitle>/<is_from_playlist>')
def vod_episode_list(api_url, show_only_subtitle, is_from_playlist):
    logger.debug('Displaying Episode List for URL: {0} - {1} - {2}'.format(
        api_url, show_only_subtitle, is_from_playlist))
    api_result_json = get_json(api_url)
    if (int(is_from_playlist) == 1):
        program_json = api_result_json['data']['playlist'][0]['track']
    else:
        program_json = api_result_json['data']['episodes']

    row_count = 0
    for row in program_json:
        row_count = +1
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if ((int(show_only_subtitle)==1) or (len(title) == 0)):
            episode_name = u'{0}'.format(subtitle)
        else:
            episode_name = u'{0} - {1}'.format(title, subtitle)

        if (len(title) == 0):
            full_episode_name = episode_name = u'{0}'.format(subtitle)
        else:
            full_episode_name = u'{0} - {1}'.format(title, subtitle)

        
        plot = row['description_clean']
        largeImaga = get_NHK_website_url(row['image_l'])
        thumb_image = get_NHK_website_url(row['image'])
        promoImage = get_NHK_website_url(row['image_promo'])
        vid_id = row['vod_id']
        #pgm_id = row['pgm_id']
        pgm_no = row['pgm_no']
        duration = row['movie_duration']

        # Check if we have an aired date
        broadcast_start_timestamp = row['onair']
        broadcast_end_timestamp = row['vod_to']

        if (broadcast_start_timestamp is not None):
            broadcast_start_timestamp = broadcast_start_timestamp/1000
            broadcast_end_timestamp = broadcast_end_timestamp/1000

            # Convert from JST to local timezone
            tokyo_tz = timezone('Asia/Tokyo')
            local_tz = get_localzone()
            
            # Parse it as JST
            broadcast_start_tokyo = tokyo_tz.localize(datetime.fromtimestamp(broadcast_start_timestamp))
            broadcast_end_tokyo  = tokyo_tz.localize(datetime.fromtimestamp(broadcast_end_timestamp))

            # Convert to local time
            broadcast_start_local = broadcast_start_tokyo.astimezone(local_tz)
            broadcast_end_local = broadcast_end_tokyo.astimezone(local_tz)

            plot = u'Broadcast on: {0} / Available until: {1}\n\n{2}'.format(
                broadcast_start_local.strftime('%Y-%m-%d'), broadcast_end_local.strftime('%Y-%m-%d'), plot)
            year = int(broadcast_start_local.strftime('%Y'))
            date_added_info_label = broadcast_start_local.strftime('%Y-%m-%d %H:%M:%S')
        else:
            year = 0
            date_added_info_label=''

        li = ListItem(episode_name)
        li.setArt(
            {'thumb': thumb_image, 'poster': promoImage, 'fanart': largeImaga})
        li.setInfo('video', {'mediatype': 'episode', 'plot': plot,
                             'duration': duration, 'episode': pgm_no, 'year': year, 'dateadded': date_added_info_label})
        li.setProperty('IsPlayable','true')                             
        addDirectoryItem(plugin.handle, plugin.url_for(show_episode, title=full_episode_name, vid_id=vid_id, episode=pgm_no, year=year, dateadded=date_added_info_label), li, False)

    endOfDirectory(plugin.handle)
    addSortMethod(plugin.handle, SORT_METHOD_TITLE)
    # Used for unit testing - only successfull if we processed at least one episode
    if (row_count > 0):
        return(vid_id)
    else:
        return(None)


# Video On Demand - Display Episode
@plugin.route('/vod/show_episode/<title>/<vid_id>/<episode>/<year>/<dateadded>')
def show_episode(title, vid_id, episode, year, dateadded):
    r = get_url(rest_url['player_url'].format(vid_id, vid_id))
    playerJS = r.text
    # Parse the output of the Player JS file for the UUID of the episode
    match = re.compile("'data-de-program-uuid','(.+?)'").findall(playerJS)
    if (match.count > 0):
        p_uuid = match[0].replace("['", "").replace("']", "")
        video_url = rest_url['video_url'].format(p_uuid)
        api_result_json = get_json(video_url)
        vod_program = api_result_json['response']['WsProgramResponse']['program']
        plot = vod_program['Description']
        duration = float(vod_program['duration'])/10
        reference_file_json = vod_program['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        episode_url = rest_url['episode_url'].format(play_path)
        logger.debug('Episode Akamai URL: {0}'.format(episode_url))
        li = ListItem(path = episode_url)
        video_info = {
            'aspect': reference_file_json['aspectRatio'],
            'width': reference_file_json['videoWidth'],
            'height': reference_file_json['videoHeight'],
        }
        li.addStreamInfo('video', video_info)
        li.setInfo('video', {'mediatype': 'episode', 'title': title, 'plot': plot,
                             'duration': duration, 'episode': episode, 'year': year, 'dateadded': dateadded})
    
        setResolvedUrl(plugin.handle, True, li)
        return(episode_url)
    else:
        logger.fatal('Could not retrieve Akamai URL for VID_ID {0}'.format(
            vid_id))
        return (None)


def run():
    plugin.run()
