# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from kodiutils import get_string, set_view_mode, set_sort_direction
import kodilogging
import xbmcgui
import xbmcplugin
from utils import get_json, get_NHK_website_url, get_url, to_local_time
from nhk_api import *
import re
from datetime import datetime, timedelta
import random


ADDON = xbmcaddon.Addon()
nhk_icon = ADDON.getAddonInfo('icon')  # icon.png in addon directory
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


# View Modes from the default Estuary skin
VIEW_MODE_INFOWALL=54
VIEW_MODE_WALL=500
VIEW_MODE_WIDELIST=55

@plugin.route('/')
def index():
    logger.debug('Creating Main Menu')
    
    ## Add menus
    add_top_stories_menu_item()
    add_on_demand_menu_item()
    add_live_stream_menu_item()

    # Set-up view
    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.endOfDirectory(plugin.handle)
    return (True)

#  Add the Top Stories menu
def add_top_stories_menu_item():
    logger.debug('Adding top stories menu item')
    
    # Getting top story
    api_result_json = get_json(rest_url['homepage_news'])
    featured_news = api_result_json['data'][0]

    fanart_image = get_NHK_website_url(featured_news['thumbnails']['middle'])
    thumb_image = get_NHK_website_url(featured_news['thumbnails']['small'])
    pgm_title = featured_news['title']
    pgm_description = featured_news['description']
    updated_at = int(featured_news['updated_at'])/1000
    updated_at_local = to_local_time(updated_at)

    title  = get_string(30010)
    output = get_string(30011)
    output = output + get_string(30012).format(pgm_title, pgm_description, updated_at_local.strftime('%H:%M'))

    li = xbmcgui.ListItem(title)
    li.setArt({'thumb': thumb_image,
               'fanart': fanart_image})
    video_info = {
        'aspect': '1.78',
        'width': '640',
        'height': '360'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        top_stories_list), li, True)
    return(True)


# Add on-demand menu item
def add_on_demand_menu_item():
    
    logger.debug('Adding on-demand menu item')
    # Getting random on-demand episode to show
    api_result_json = get_json(rest_url['homepage_ondemand'])
    featured_episodes = api_result_json['data']['items']

    no_of_epsisodes = len(featured_episodes)
    featured_episode = random.randint(0, no_of_epsisodes-1)
    program_json = featured_episodes[featured_episode]
    fanart_image = get_NHK_website_url(program_json['image_pc'])
    thumb_image = get_NHK_website_url(program_json['image_sp'])
    pgm_title = program_json['pgm_title_clean']

    title = get_string(30020)
    output = get_string(30021)
    output = output + get_string(30022).format(pgm_title)
    li = xbmcgui.ListItem(title)
    li.setArt({'thumb': thumb_image,
               'fanart': fanart_image})
    video_info = {
        'aspect': '1.78',
        'width': '1920',
        'height': '1080'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_index), li, True)
    return(True)
    

# Add live stream menu item
def add_live_stream_menu_item():
    logger.debug('Adding live stream menu item')
    livestream_url = rest_url['live_stream_url']
    logger.debug('1080p Livestream Akamai URL: {0}'.format(livestream_url))
    
    title = get_string(30030)
    li = xbmcgui.ListItem(title)
    
    logger.debug('Retrieving live stream next shows')
    api_result_json = get_json(rest_url['get_live_stream_next_shows'])
    program_json = api_result_json['channel']['item']

    # Currently playing
    
    row_count = 0
    for row in program_json:
        row_count = row_count+1

        #Schedule Information
        pubDate = int(row['pubDate'])/1000
        endDate = int(row['endDate'])/1000

        broadcast_start_local = to_local_time(pubDate)
        broadcast_end_local = to_local_time(endDate)
        
        if (row_count == 1):
            #Live porgram
            fanart_image = get_NHK_website_url(row['thumbnail'])
            thumb_image = get_NHK_website_url(row['thumbnail_s'])

            # Title and Description
            full_title = '{0}\n\n{1}'.format(row['title'], row['description'])
            plot = u'{0}-{1}: {2}'.format(
                    broadcast_start_local.strftime('%H:%M'), broadcast_end_local.strftime('%H:%M'), full_title)
            output = plot + get_string(30031)
        else:
            #  Upcoming programs
            #  Only Title
            full_title = row['title']
            plot = u'{0}-{1}: {2}'.format(
                    broadcast_start_local.strftime('%H:%M'), broadcast_end_local.strftime('%H:%M'), full_title)
            output = output + '\n' + plot


    output = output + get_string(30032).format(datetime.now().strftime('%H:%M'))
        
    li.setArt({'thumb': thumb_image,
               'fanart': fanart_image})
    video_info = {
        'aspect': '1.78',
        'width': '1920',
        'height': '1080'
    }
    li.addStreamInfo('video', video_info)
    li.setInfo('video', {'mediatype': 'episode', 'plot': output})
    xbmcplugin.addDirectoryItem(plugin.handle, livestream_url,li, False)
    return(True)

#
# Video On Demand Mennu
#

@plugin.route('/vod/index')
def vod_index():
    logger.debug('Creating Video On Demand Menu')
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_programs), xbmcgui.ListItem(get_string(30040), iconImage=nhk_icon), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_categories), xbmcgui.ListItem(get_string(30041), iconImage=nhk_icon), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_playlists), xbmcgui.ListItem(get_string(30042), iconImage=nhk_icon), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_latest_episodes'], 0, 0, xbmcplugin.SORT_METHOD_DATEADDED), xbmcgui.ListItem(get_string(30043), iconImage=nhk_icon), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_most_watched_episodes'],0, 0, xbmcplugin.SORT_METHOD_NONE), xbmcgui.ListItem(get_string(30044), iconImage=nhk_icon), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        vod_episode_list, rest_url['get_all_episodes'], 0, 0, xbmcplugin.SORT_METHOD_TITLE), xbmcgui.ListItem(get_string(30045), iconImage=nhk_icon), True)
    set_view_mode(VIEW_MODE_WIDELIST)
    xbmcplugin.endOfDirectory(plugin.handle)
    return(True)



# By Program (Programs Tab on NHK World Site)
@plugin.route('/vod/programs/')
def vod_programs():

    api_result_json = get_json(rest_url['get_programs'])
    program_json = api_result_json['vod_programs']['programs']
    row_count = 0
    for row in program_json:
        row_count = row_count+1
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
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image, 'poster': poster_image,
                       'fanart': poster_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title, 'plot': plot})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 1, 0, xbmcplugin.SORT_METHOD_TITLE), li, True)

    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)
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
        row_count = row_count+1
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
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 0, 0, xbmcplugin.SORT_METHOD_TITLE), li, True)

    
    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_WALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)
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
        row_count = row_count+1
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
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': thumb_image})
            li.setInfo('video', {'mediatype': 'videos',
                                 'title': title})
            logger.debug('Creating Directory Item {0} - {1}'.format(
                api_url, title.encode('ascii', 'ignore')))

            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
                vod_episode_list, api_url, 0, 1, xbmcplugin.SORT_METHOD_TITLE), li, True)
    
    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_WALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)

    # Return last valid program URL - useful for debugging
    if (row_count > 0):
        return(api_url)
    else:
        return(None)


# Video On Demand - Episode List
@plugin.route('/vod/episode_list/<path:api_url>/<show_only_subtitle>/<is_from_playlist>/<sort_method>/')
def vod_episode_list(api_url, show_only_subtitle, is_from_playlist, sort_method):
    logger.debug('Displaying Episode List for URL: {0} - {1} - {2}'.format(
        api_url, show_only_subtitle, is_from_playlist))
    api_result_json = get_json(api_url)
    if (int(is_from_playlist) == 1):
        program_json = api_result_json['data']['playlist'][0]['track']
    else:
        program_json = api_result_json['data']['episodes']

    row_count = 0
    for row in program_json:
        row_count = row_count+1
        title = row['title_clean']
        subtitle = row['sub_title_clean']

        if ((int(show_only_subtitle)==1) or (len(title) == 0)):
            episode_name = u'{0}'.format(subtitle)
        else:
            episode_name = u'{0} - {1}'.format(title, subtitle)

        plot = row['description_clean']
        largeImaga = get_NHK_website_url(row['image_l'])
        thumb_image = get_NHK_website_url(row['image'])
        promoImage = get_NHK_website_url(row['image_promo'])
        vid_id = row['vod_id']
        pgm_no = row['pgm_no']
        duration = row['movie_duration']

        # Check if we have an aired date
        broadcast_start_timestamp = row['onair']
        broadcast_end_timestamp = row['vod_to']

        if (broadcast_start_timestamp is not None):
            broadcast_start_timestamp = int(broadcast_start_timestamp)/1000
            broadcast_end_timestamp = int(broadcast_end_timestamp)/1000

            # Convert to local time
            broadcast_start_local = to_local_time(broadcast_start_timestamp)
            broadcast_end_local = to_local_time(broadcast_end_timestamp)

            plot = get_string(30050).format(
                broadcast_start_local.strftime('%Y-%m-%d'), broadcast_end_local.strftime('%Y-%m-%d'), plot)
            year = int(broadcast_start_local.strftime('%Y'))
            date_added_info_label = broadcast_start_local.strftime('%Y-%m-%d %H:%M:%S')
        else:
            year = 0
            date_added_info_label=''

        li = xbmcgui.ListItem(episode_name)
        li.setArt(
            {'thumb': thumb_image, 'poster': promoImage, 'fanart': largeImaga})
        li.setInfo('video', {'mediatype': 'episode', 'plot': plot,
                             'duration': duration, 'episode': pgm_no, 'year': year, 'dateadded': date_added_info_label})
        li.setProperty('IsPlayable','true')                             
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_episode, vid_id=vid_id, year=year, dateadded=date_added_info_label), li, False)

    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_INFOWALL)
    sort_method = int(sort_method)
    xbmcplugin.addSortMethod(plugin.handle, sort_method)

    # If we sort by date added, make sure sort direction is descending (e.g. for latest episodes)
    if (sort_method == xbmcplugin.SORT_METHOD_DATEADDED):
        set_sort_direction('Descending')

    xbmcplugin.endOfDirectory(plugin.handle)

    # Used for unit testing - only successfull if we processed at least one episode
    if (row_count > 0):
        return(vid_id)
    else:
        return(None)


# Video On Demand - Display Episode
@plugin.route('/vod/show_episode/<vid_id>/<year>/<dateadded>/')
def show_episode(vid_id, year, dateadded):
    r = get_url(rest_url['player_url'].format(vid_id, vid_id))
    playerJS = r.text
    # Parse the output of the Player JS file for the UUID of the episode
    program_uuid = re.compile("'data-de-program-uuid','(.+?)'").findall(playerJS)
    if (program_uuid.count > 0):
        video_url = rest_url['video_url'].format(program_uuid[0])

        # Get episode detail
        episode_json = get_json(rest_url['get_episode_detail'].format(vid_id))
        episode_detail = episode_json['data']['episodes'][0]
        title = episode_detail['title_clean'] 
        plot = episode_detail['description_clean']
        episode = episode_detail['pgm_no']
        duration = episode_detail['movie_duration']
        
        # Get episode URL and video information
        api_result_json = get_json(video_url)
        vod_program = api_result_json['response']['WsProgramResponse']['program']
        reference_file_json = vod_program['asset']['referenceFile']
        play_path = reference_file_json['rtmp']['play_path'].split('?')[0]
        episode_url = rest_url['episode_url'].format(play_path)
        logger.debug('Episode Akamai URL: {0}'.format(episode_url))
        li = xbmcgui.ListItem(path = episode_url)
        video_info = {
            'aspect': reference_file_json['aspectRatio'],
            'width': reference_file_json['videoWidth'],
            'height': reference_file_json['videoHeight'],
        }
        li.addStreamInfo('video', video_info)
        li.setInfo('video', {'mediatype': 'episode', 'title': title, 'plot': plot,
                             'duration': duration, 'episode': episode, 'year': year, 'dateadded': dateadded})
    
        xbmcplugin.setResolvedUrl(plugin.handle, True, li)
        return(episode_url)
    else:
        logger.fatal('Could not retrieve Akamai URL for VID_ID {0}'.format(
            vid_id))
        return (None)

# Top Stories - List
@plugin.route('/vod/top_stories_list/')
def top_stories_list():
    logger.debug('Displaying Top Stories list')
    api_result_json = get_json(rest_url['homepage_news'])
    MAX_ROW_COUNT = 9 
    result_row_count = len(api_result_json['data'])
    # Only display MAX ROWS
    if (result_row_count < MAX_ROW_COUNT):
        MAX_ROW_COUNT = result_row_count
    
    for row_count in range(0, MAX_ROW_COUNT-1):
        row = api_result_json['data'][row_count]
        if row['videos'] is not None:
            # Only show top-stories that have a video attached to them
            fanart_image = get_NHK_website_url(row['thumbnails']['middle'])
            thumb_image = get_NHK_website_url(row['thumbnails']['small'])
            vid_id = row['id']
            video_xml_url = rest_url['get_news_xml'].format(vid_id)
            video_response = get_url(video_xml_url)
            video_xml = str(video_response.content)
            start_pos = video_xml.find(vid_id)
            end_pos = video_xml.find('HQ')
            video_file = video_xml[start_pos:end_pos]
            video_url = rest_url['news_url'].format(video_file)
            title = row['title']
            plot = row['description']
            duration =row['videos']['duration']
            updated_at = int(row['updated_at'])/1000
            updated_at_local = to_local_time(updated_at)
            date_added_info_label = updated_at_local.strftime('%Y-%m-%d %H:%M:%S')
            year = int(updated_at_local.strftime('%Y'))

            time_difference_hours = datetime.now().hour-updated_at_local.hour
            if (time_difference_hours<=1):
                time_difference = get_string(30060).format(time_difference_hours)
            else:
                time_difference = get_string(30061).format(time_difference_hours)

            minutes = int(duration/60)
            seconds = duration - (minutes*60)
            duration_text = '{0}m {1}s'.format(minutes, seconds)
            plot = u'{0} | {1}\n\n{2}'.format(duration_text, time_difference, plot)
        
            li = xbmcgui.ListItem(path = video_url)
            
            li.setArt({'thumb': thumb_image,
                    'fanart': fanart_image})
            video_info = {
                'aspect': '1.78',
                'width': '640',
                'height': '360'
            }
            li.addStreamInfo('video', video_info)
            li.setArt({'thumb': thumb_image, 'fanart': fanart_image})
            li.setInfo('video', {'mediatype': 'episode', 'title': title, 'plot': plot,
                                'duration': duration, 'year': year, 'dateadded': date_added_info_label})
            li.setProperty('IsPlayable','true')
            xbmcplugin.addDirectoryItem(plugin.handle, video_url, li, False,totalItems=MAX_ROW_COUNT)
        
    xbmcplugin.setContent(plugin.handle, 'videos')
    set_view_mode(VIEW_MODE_INFOWALL)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_DATEADDED)
    set_sort_direction('Descending')
    xbmcplugin.endOfDirectory(plugin.handle)

    # Used for unit testing - only successfull if we processed at least top story
    if (row_count > 0):
        return(row_count)
    else:
        return(0)

def run():
    plugin.run()
