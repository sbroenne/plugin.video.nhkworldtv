# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import re
import requests
import requests_cache
from kodi_six import xbmc, xbmcaddon
from . import api_keys
from . import cache_api
from datetime import datetime
import time
import pytz
from tzlocal import get_localzone

# Get Plug-In path
ADDON = xbmcaddon.Addon()
plugin_path = ADDON.getAddonInfo('path')
if (len(plugin_path) > 0):
    # Running within Kodi - use that path
    db_name = '{0}/nhk_world_cache'.format(plugin_path)
    UNIT_TEST = False
else:
    # Running under unit test
    db_name = 'nhk_world_cache'
    UNIT_TEST = True

URL_CACHE_MINUTES = ADDON.getSettingInt('url_cache_minutes')
# Enforce minimu 60 minutes caching
if URL_CACHE_MINUTES < 60:
    URL_CACHE_MINUTES = 60

# Install the cache for requests
requests_cache.install_cache(db_name,
                             backend='sqlite',
                             expire_after=URL_CACHE_MINUTES * 60)
requests_cache.remove_expired_responses()

# Instantiate request session
s = requests.Session()
# Act like a browser
headers = {
    'agent':
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/82.0.4080.0 Mobile Safari/537.36'
}
s.headers = headers


def check_url_exists(url):
    """Check if a URL exists of it returns a 404

    Arguments:
        url {str} -- URL to check
    """
    with s.cache_disabled():
        r = s.get(url)
        if (r.status_code == 404):
            return (False)
        else:
            return (True)


def get_json(url, cached=True):
    """ Get JSON object from a URL with improved error handling """
    r = get_url(url, cached)
    try:
        result = r.json()
        xbmc.log(
            'Successfully loaded JSON from API: {0} with Status {1}'.format(
                r.url, r.status_code))
        return (result)
    finally:
        # Failure - no way to handle - probably an issue with the NHK Website
        # Raise exception
        r.raise_for_status()


def get_url(url, cached=True):
    """ Get a URL with automatic retries
        NHK sometimes have intermittent problems with 502 Bad Gateway """

    # Populate request_params if needed
    if (api_keys.NHK_API_BASE_URL in url):
        request_params = {'apikey': api_keys.NHK_API_KEY}
    elif (api_keys.CACHE_API_BASE_URL in url):
        request_params = {'code': api_keys.CACHE_API_KEY}
    else:
        request_params = None

    # maximum number of retries
    max_retries = 3
    current_try = 1
    while (current_try <= max_retries):
        # Only add the API key for API Calls

        # Use cached or non-cached result
        if (cached):
            # Use session cache
            if (request_params is not None):
                r = s.get(url, params=request_params)
            else:
                r = s.get(url)
        else:
            with s.cache_disabled():
                if (request_params is not None):
                    r = s.get(url, params=request_params)
                else:
                    r = s.get(url)

        # Make an API Call
        xbmc.log('Making API Call {0} ({1} of {2})'.format(
            r.url, current_try, max_retries))

        if (r.status_code == 200):
            # Call was successfull
            xbmc.log('Successfully fetched URL/API: {0} - Status {1} \
                 - Retrieved from cache {2}'.format(r.url, r.status_code,
                                                    r.from_cache))
            return (r)
        elif (r.status_code == 502):
            # Bad Gateway
            if (current_try == max_retries):
                # Max retries reached - still could not get url
                # Failure - no way to handle - probably an issue
                # with the NHK Website
                # Raise exception
                xbmc.log(
                    'Could not get URL {0} - HTTP Status Code {1} \
                    - Retries {2}'.format(r.url, r.status_code, current_try),
                    xbmc.LOGFATAL)
                r.raise_for_status()
            else:
                # Wait for n seconds and then try again
                xbmc.log(
                    'Failure fetching URL: {0} with Status {1})'.format(
                        r.url, r.status_code), xbmc.LOGWARNING)
                current_try = current_try + 1
        else:
            # Other error
            xbmc.log(
                'Could not get URL {0} - HTTP Status Code {1} - Retries {2}'.
                format(r.url, r.status_code, current_try), xbmc.LOGFATAL)
            r.raise_for_status()
            exit


def get_NHK_website_url(path):
    """ Return a full URL from the partial URLs in the JSON results """
    nhk_website = api_keys.NHK_BASE_URL
    return nhk_website + path


def to_local_time(timestamp):
    """ Convert from a UNIX timestamp to a valid date time """
    local_time = datetime.fromtimestamp(timestamp)
    return (local_time)


def get_episode_name(title, subtitle):
    """ Construct an epsidode name from the title and the subtitle"""
    if len(subtitle) == 0:
        episode_name = '{0}'.format(title)
    else:
        episode_name = '{0} - {1}'.format(title, subtitle)
    return (episode_name)


def get_top_stories_play_path(xmltext):
    """ Extracts the play path from a top story XML file """
    find = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/(.+?)HQ'

    matches = re.compile(find).findall(xmltext)
    if len(matches) == 1:
        play_path = matches[0]
    else:
        play_path = None
    return play_path


def get_ataglance_play_path(xmltext):
    """ Extracts the play path from a At a Glance XML file """
    find = '<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/(.+?)</file.high>'

    matches = re.compile(find).findall(xmltext)
    if len(matches) == 1:
        play_path = matches[0]
    else:
        play_path = None
    return play_path


def get_news_program_play_path(xmltext):
    """ Extracts the play path from a news program file """
    find = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/programs/(.+?)hq.mp4'

    matches = re.compile(find).findall(xmltext)
    if len(matches) == 1:
        play_path = matches[0]
    else:
        play_path = None
    return play_path


def get_program_metdadata_cache(max_items):
    """Use NHK World TV Cloud Service to speed-up episode URLlookup.
    The service runs on Azure in West Europe but should still speed up
    the lookup process dramatically since it uses a pre-loaded cache

    Arguments:
        max_items {int} -- Amount of items to retrievve

    Returns:
        {dict} -- A JSON dict with the cache items
    """
    xbmc.log('Getting vod_id/program metadata cache from Azure')
    cache = get_json(
        cache_api.rest_url['cache_get_program_list'].format(max_items))
    return (cache)


def get_schedule_title(start_date, end_date, title):
    """Returns a title formatted for a schedule (e.g. live stream, live)

    Arguments:
        start_date {datetime} -- Start date
        end_date {datetime} -- End date
        title {unicode} -- Title
     Returns:
        {unicode} -- 11:30-12:30: Journeys in Japan
    """
    return ('{0}-{1}: {2}'.format(start_date.strftime('%H:%M'),
                                  end_date.strftime('%H:%M'), title))


def get_timestamp_from_datestring(datestring):
    """Converts a news item date string into a NHK timestamp
    NHK Timestamp ? Unix Timestamp * 1000

    Arguments:
        date_string {unicode} -- News item date string (e.g. '20200416130000')
     Returns:
        {unicode} -- NHK Timestamp (e.g. 1587008460000)
    """
    # Convert news date string to a Tokyo date
    tokyo = pytz.timezone('Asia/Tokyo')
    tokyo_dt = datetime(year=int(datestring[0:4]),
                        month=int(datestring[4:6]),
                        day=int(datestring[6:8]),
                        hour=int(datestring[8:10]),
                        minute=int(datestring[10:12]),
                        second=int(datestring[12:14]),
                        tzinfo=tokyo)
    # Convert to local time zone
    local_tz = get_localzone()
    local_dt = tokyo_dt.astimezone(local_tz)
    # Convert to NHK timestamp that can be used to populate
    # episode.broadcast_start_date etc.
    timestamp = int(time.mktime(local_dt.timetuple()) * 1000)
    return (timestamp)
