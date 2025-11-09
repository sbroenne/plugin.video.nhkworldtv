"""
Commonly used utility functions
"""

import re
import time
from datetime import datetime

import pytz
import xbmcaddon
from tzlocal import get_localzone

UNIT_TEST = False

# Get Plug-In path
ADDON = xbmcaddon.Addon()
PLUGIN_PATH = ADDON.getAddonInfo("path")
if len(PLUGIN_PATH) == 0:
    # Running under unit test
    UNIT_TEST = True


def to_local_time(timestamp: int) -> datetime:
    """Convert from a UNIX timestamp to a valid datetime

    Args:
        timestamp: Unix timestamp in seconds

    Returns:
        datetime object in local timezone
    """

    try:
        local_time = datetime.fromtimestamp(timestamp)
    except (OverflowError, ValueError):
        local_time = datetime.max

    return local_time


def get_episode_name(title: str, subtitle: str) -> str:
    """Construct an episode name from the title and the subtitle

    Args:
        title: Episode title
        subtitle: Episode subtitle

    Returns:
        Formatted episode name
    """
    if len(subtitle) == 0:
        subtitle = subtitle.replace("<p></p>", "")
        episode_name = f"{title}"
    else:
        title = title.replace("<p></p>", "")
        episode_name = f"{title} - {subtitle}"
    return episode_name


def get_topstories_play_path(xml_text: str) -> str | None:
    """Extracts the play path from a Top Stories XML file

    Args:
        xml_text: XML content as string or direct RTMP URL

    Returns:
        Play path string or None if not found
    """
    find = "rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/(.+?)HQ"

    matches = re.compile(find).findall(xml_text)
    if len(matches) == 1:
        play_path: str | None = matches[0]
    else:
        play_path = None
    return play_path


def get_ataglance_play_path(xml_text: str) -> str | None:
    """Extracts the play path from a At a Glance XML file

    Args:
        xml_text: XML content as string

    Returns:
        Play path string or None if not found
    """
    find = "<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/(.+?)</file.high>"

    matches = re.compile(find).findall(xml_text)
    if len(matches) == 1:
        play_path: str | None = matches[0]
    else:
        play_path = None
    return play_path


def get_schedule_title(start_date: datetime, end_date: datetime, title: str) -> str:
    """Returns a title formatted for a schedule (e.g. live stream, live)

    Arguments:
        start_date: Start date
        end_date: End date
        title: Title

    Returns:
        Formatted title like "11:30-12:30: Journeys in Japan"
    """
    return f"{start_date.strftime('%H:%M')}-{end_date.strftime('%H:%M')}: {title}"


def get_timestamp_from_datestring(datestring: str) -> int:
    """Converts a news item date string into a NHK timestamp
    NHK Timestamp = Unix Timestamp * 1000

    Arguments:
        datestring: News item date string (e.g. '20200416130000')

    Returns:
        NHK Timestamp (e.g. 1587008460000)
    """
    # Convert news date string to a Tokyo date
    tokyo = pytz.timezone("Asia/Tokyo")
    tokyo_dt = datetime(
        year=int(datestring[0:4]),
        month=int(datestring[4:6]),
        day=int(datestring[6:8]),
        hour=int(datestring[8:10]),
        minute=int(datestring[10:12]),
        second=int(datestring[12:14]),
        tzinfo=tokyo,
    )

    # Convert to local time zone
    local_tz = get_localzone()
    local_dt = tokyo_dt.astimezone(local_tz)
    # Convert to NHK timestamp that can be used to populate
    # episode.broadcast_start_date etc.
    timestamp = int(time.mktime(local_dt.timetuple()) * 1000)
    return timestamp


def format_plot(line1: str, line2: str) -> str:
    """Format the plot field

    Args:
        line1: First line
        line2: Second line

    Returns:
        Formatted plot field
    """
    return f"{line1}\n\n{line2}"
