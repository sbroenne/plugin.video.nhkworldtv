from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import re
import requests
import requests_cache
import xbmc
import xbmcaddon
from . import api_keys
from . import cache_api
import datetime

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
    local_time = datetime.datetime.fromtimestamp(timestamp)
    return (local_time)


def get_episode_name(title, subtitle):
    """ Construct an epsidode name from the title and the subtitle"""
    if len(subtitle) == 0:
        episode_name = '{0}'.format(title)
    else:
        episode_name = '{0} - {1}'.format(title, subtitle)
    return (episode_name)


def get_episodelist_title(title, total_episodes):
    """ Gets a formated episode list title, e.g. '1 episode' or '2 episodes'"""
    if (total_episodes == 1):
        episodelist_title = '{0} - {1} episode'.format(title, total_episodes)
    else:
        episodelist_title = '{0} - {1} episodes'.format(title, total_episodes)
    return (episodelist_title)


def get_top_stories_play_path(xmltext):
    """ Extracts the play path from a top story XML file """
    find = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/(.+?)HQ'

    matches = re.compile(find).findall(xmltext)
    play_path = matches[0]
    return play_path


def get_ataglance_play_path(xmltext):
    """ Extracts the play path from a At a Glance XML file """
    find = '<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/(.+?)</file.high>'

    matches = re.compile(find).findall(xmltext)
    play_path = matches[0]
    return play_path


def get_news_program_play_path(xmltext):
    """ Extracts the play path from a news program file """
    find = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/programs/(.+?)hq.mp4'

    matches = re.compile(find).findall(xmltext)
    play_path = matches[0]
    return play_path


def get_program_metdadata_cache(max_items):
    """
    #Use NHK World TV Cloud Service to speed-up episode URLlookup
    The service runs on Azure in West Europe but should still speed up
    the lookup process dramatically since it uses a pre-loaded cache
    """
    xbmc.log('Getting vod_id/program metadata cache from Azure')
    cache = get_json(
        cache_api.rest_url['cache_get_program_list'].format(max_items))
    return (cache)
