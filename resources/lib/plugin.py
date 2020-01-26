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
from datetime import datetime
import re


ADDON = xbmcaddon.Addon()
nhk_icon = ADDON.getAddonInfo('icon')  # icon.png in addon directory
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


@plugin.route('/')
def index():
    logger.debug('Creating Main Menu')
    addDirectoryItem(plugin.handle, plugin.url_for(
        vod_index), ListItem("NHK World On Demand", iconImage=nhk_icon), True)
    add_live_stream()
    endOfDirectory(plugin.handle)
    return (True)

# Add live stream URL


def add_live_stream():

    livestream_url = 'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_4M.m3u8'
    logger.debug('1080p Livestream Akamai URL: {0}'.format(livestream_url))
    title = 'NHK World Live Stream'
    poster_image = nhk_icon
    thumb_image = nhk_icon
    li = ListItem(title)
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
            episode = u'{0}'.format(subtitle)
        else:
            episode = u'{0} - {1}'.format(title, subtitle)

        if (len(title) == 0):
            fullEpisodeName = u'{0}'.format(subtitle)
        else:
            fullEpisodeName = u'{0} - {1}'.format(title, subtitle)

        plot = row['description_clean']
        largeImaga = get_NHK_website_url(row['image_l'])
        thumb_image = get_NHK_website_url(row['image'])
        promoImage = get_NHK_website_url(row['image_promo'])
        vid_id = row['vod_id']
        pgm_id = row['pgm_id']
        pgm_no = row['pgm_no']
        duration = row['movie_duration']

        # Check if we have an aired date
        onair = row['onair']
        if (onair is not None):
            utc_time = datetime.utcfromtimestamp(onair/1000)
            plot = u'Aired: {0} ({1}-{2})\n\n{3}'.format(
                utc_time.strftime('%Y-%m-%d'), pgm_id, pgm_no, plot)
            year = int(utc_time.strftime('%Y'))
            dateadded = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            year = 0
            dateadded = ''

        li = ListItem(episode)
        li.setArt(
            {'thumb': thumb_image, 'poster': promoImage, 'fanart': largeImaga})
        li.setInfo('video', {'mediatype': 'episode', 'title': fullEpisodeName, 'plot': plot,
                             'duration': duration, 'episode': pgm_no, 'year': year, 'dateadded': dateadded})
        li.setProperty('IsPlayable','true')                             
        addDirectoryItem(plugin.handle, plugin.url_for(show_episode, title=title, vid_id=vid_id,
                                                       plot=plot, duration=duration, episode=episode, year=year, dateadded=dateadded), li, False)

    endOfDirectory(plugin.handle)
    setContent(plugin.handle, 'videos')
    addSortMethod(plugin.handle, SORT_METHOD_TITLE)
    # Used for unit testing - only successfull if we processed at least one episode
    if (row_count > 0):
        return(vid_id)
    else:
        return(None)


# Video On Demand - Display Episode
@plugin.route('/vod/show_episode/<title>/<vid_id>/<plot>/<duration>/<episode>/<year>/<dateadded>')
def show_episode(title, vid_id, plot, duration, episode, year, dateadded):
    r = get_url(
        'https://movie-s.nhk.or.jp/v/refid/nhkworld/prefid/{0}?embed=js&targetId=videoplayer&de-responsive=true&de-callback-method=nwCustomCallback&de-appid={1}&de-subtitle-on=false'.format(vid_id, vid_id))
    playerJS = r.text
    # Parse the output of the Player JS file for the UUID of the episode
    match = re.compile("'data-de-program-uuid','(.+?)'").findall(playerJS)
    if (match.count > 0):
        p_uuid = match[0].replace("['", "").replace("']", "")
        video_url = 'https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v={0}'.format(
            p_uuid)
        api_result_json = get_json(video_url)
        vod_program = api_result_json['response']['WsProgramResponse']['program']
        reference_file_json = vod_program['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        episode_url = 'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/{0}/chunklist.m3u8'.format(
            play_path)
        logger.debug('Episode Akamai URL: {0}'.format(episode_url))
        poster_image = vod_program['posterUrl']
        thumb_image = vod_program['thumbnailUrl']
        li = ListItem(path = episode_url)
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
    
        li.setProperty('IsPlayable','true')
        setResolvedUrl(plugin.handle, True, li)
        return(episode_url)
    else:
        logger.fatal('Could not retrieve Akamai URL for VID_ID {0}'.format(
            vid_id))
        return (None)


def run():
    plugin.run()
