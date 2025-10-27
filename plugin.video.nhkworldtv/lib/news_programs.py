"""
News programs
"""
import xml.etree.ElementTree as ET

import xbmc
from requests.models import HTTPError

from . import kodiutils, nhk_api, url, utils
from .episode import Episode


def get_programs():
    """Get the list of news programs

    Returns:
        [list]: List of news programs, empty list if API call fails
    """
    xbmc.log("Getting news programs from NHK")
    api_result_json = url.get_json(nhk_api.rest_url["news_program_config"], False)
    
    if api_result_json is None or "config" not in api_result_json:
        xbmc.log("news_programs.get_programs: Failed to load news program config", xbmc.LOGERROR)
        kodiutils.show_notification("NHK World TV", "Unable to load News Programs.")
        return []
    
    if "programs" not in api_result_json["config"]:
        xbmc.log("news_programs.get_programs: No programs in config", xbmc.LOGERROR)
        kodiutils.show_notification("NHK World TV", "Unable to load News Programs.")
        return []
    
    news_programs = api_result_json["config"]["programs"]
    row_count = 0
    episodes = []

    root = None

    for news_program in news_programs:
        row_count = row_count + 1
        news_program_xml = None
        news_program_id = news_program.get("id", "")
        if not news_program_id:
            continue
            
        api_url = nhk_api.rest_url["news_program_xml"].format(news_program_id)

        # Get the News Program URL from NHK - sometimes it doesn't exist
        # Errors will be ignored and the offending program will not be added
        # https://github.com/sbroenne/plugin.video.nhkworldtv/issues/9
        try:
            request = url.get_url(api_url, False)
            if request.status_code == 200:
                news_program_xml = request.text
            else:
                xbmc.log(f"news_programs.get_programs: Could not load Program XML {news_program_id} (status {request.status_code})", xbmc.LOGWARNING)
                continue
        except HTTPError as e:
            xbmc.log(f"news_programs.get_programs: HTTPError loading Program XML {news_program_id}: {str(e)}", xbmc.LOGWARNING)
            continue
        except Exception as e:
            xbmc.log(f"news_programs.get_programs: Error loading Program XML {news_program_id}: {str(e)}", xbmc.LOGWARNING)
            continue
        else:
            if not news_program_xml:
                xbmc.log(f"news_programs.get_programs: Empty XML for program {news_program_id}", xbmc.LOGWARNING)
                continue
                
            # Sometimes the XML is invalid, add error handling
            try:
                root = ET.fromstring(news_program_xml)
            except ET.ParseError as e:
                xbmc.log(f"news_programs.get_programs: Could not parse Program XML {news_program_id}: {str(e)}", xbmc.LOGWARNING)
                continue
            else:
                # Add program - with null safety for XML elements
                file_high = root.find("file.high")
                if file_high is None or file_high.text is None:
                    xbmc.log(f"news_programs.get_programs: No file.high element for {news_program_id}", xbmc.LOGWARNING)
                    continue
                    
                play_path = nhk_api.rest_url["news_programs_video_url"].format(
                    utils.get_news_program_play_path(file_high.text)
                )
                episode = Episode()
                vod_id = f"news_program_{news_program_id}"
                episode.vod_id = vod_id

                # Extract the Title
                break_string = "<br />"
                description_elem = root.find("description")
                description = description_elem.text if description_elem is not None and description_elem.text else ""
                
                if break_string in description:
                    lines = description.split(break_string, 1)
                    episode.title = lines[0]
                    # Extract the broadcast time and convert it to local time
                    date_string = lines[1].strip()
                    episode.broadcast_start_date = utils.get_timestamp_from_datestring(
                        (date_string)
                    )
                    episode.plot_include_time_difference = True
                else:
                    episode.title = description if description else news_program_id

                episode.plot = ""
                episode.fanart = news_program.get("image", "")
                episode.thumb = news_program.get("image", "")
                
                media_time = root.find("media.time")
                episode.duration = media_time.text if media_time is not None and media_time.text else "0"
                episode.video_info = kodiutils.get_sd_video_info()
                episode.is_playable = True
                episodes.append((play_path, episode.kodi_list_item, False))

    return episodes
