"""
URL / Request handling
"""
import sqlite3
import time

import requests
import requests_cache
import xbmc
import xbmcaddon
from requests.models import Response

# Get Plug-In path
ADDON = xbmcaddon.Addon()
PLUGIN_PATH = ADDON.getAddonInfo('path')
# Running within Kodi - use that path
# Get Plug-In information
DB_NAME = f"{PLUGIN_PATH}/nhk_world_cache"
URL_CACHE_MINUTES = ADDON.getSettingInt('url_cache_minutes')
if len(PLUGIN_PATH) == 0:
    # Running under unit test - overwrite location of DB
    DB_NAME = "nhk_world_cache"
    URL_CACHE_MINUTES = 60

# Enforce minimum 60 minutes caching
if URL_CACHE_MINUTES < 60:
    URL_CACHE_MINUTES = 60

# Install the cache for requests
requests_cache.install_cache(DB_NAME,
                             backend="sqlite",
                             expire_after=URL_CACHE_MINUTES * 60)
# Note: remove_expired_responses() was removed in newer versions of requests-cache
# The cache automatically handles expiration with the expire_after parameter

# Instantiate request session
session = requests.Session()
# Act like a browser
headers = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182"
}
session.headers = headers


def check_url_exists(url):
    """Check if a URL exists of it returns a 404

    Arguments:
        url {str} -- URL to check
    """
    with session.cache_disabled():
        request = session.get(url)
        if request.status_code == 404:
            return False
        else:
            return True


def get_json(url, cached=True):
    """ Get JSON object from a URL with improved error handling

    Args:
        url ([str]): URL to retrieve
        cached (bool, optional): Use request_cache. Defaults to True.

    Returns:
        [dict]: JSON dictionary
    """
    request = get_url(url, cached)
    if request.status_code == 200:
        try:
            result = request.json()
            xbmc.log(f"Successfully loaded JSON from API: {url}")
            return result
        except ValueError:
            # Failure - no way to handle - probably an issue with the NHK API
            xbmc.log(f"Could not parse JSON from API: {url}")
    else:
        # Failure - could not connect to site
        xbmc.log(f"Could not connect to API: {url}")


def request_url(url, cached=True):
    """ HELPER: Request URL with handling basic error conditions

    Args:
        url ([str]): URL to retrieve
        cached (bool, optional): Use request_cache. Defaults to True.

    Returns:
        [response]: Response object - can be None
    """

    request = Response()

    try:
        # Use cached or non-cached result
        if cached:
            # Use session cache
            request = session.get(url)
        else:
            with session.cache_disabled():
                request = session.get(url)
        return request
    except requests.ConnectionError:
        # Could not establish connection at all
        request.status_code = 10001
    except sqlite3.OperationalError:
        # Catch transient requests-cache SQL Lite error
        # This is a race condition I think, it takes time for
        # requests-cache to create the response table
        # but it doesn't wait for this internally
        # so sometimes a call can be made
        # before the the table has been created
        # This will fix itself shortly (on the next call)
        xbmc.log("url.request_url: Swallowing sqlite3.OperationalError")
        request.status_code = 10002
    return request


def get_url(url, cached=True):
    """Get a URL with automatic retries
        NHK sometimes have intermittent problems with 502 Bad Gateway

    Args:
        url ([str]): URL to retrieve
        cached (bool, optional): Use request_cache. Defaults to True.

    Returns:
        [response]: Response object
    """

    # maximum number of retries
    max_retries = 3
    current_try = 1

    while current_try <= max_retries:
        # Make an API Call
        xbmc.log(f"Fetching URL:{url} ({current_try} of {max_retries})")

        request = request_url(url, cached)
        status_code = request.status_code

        if status_code == 200:
            # Call was successful
            xbmc.log(f"Successfully fetched URL: {url} - Status {status_code} \
                    - Retrieved from cache {request.from_cache}")
            break

        elif (status_code == 502 or status_code == 10002):
            # Bad Gateway or SQL Lite Operational exception - can be retried
            if current_try == max_retries:
                # Max retries reached - still could not get url
                # Failure - no way to handle - probably an issue
                # with the NHK Website
                xbmc.log(
                    f"FATAL: Could not get URL {url} after {current_try} retries",
                    xbmc.LOGDEBUG)
                break
            else:
                # Try again - this usually fixes the error with
                # the next request
                xbmc.log(
                    f"Temporary failure fetching URL: {url} with Status {status_code})",
                    xbmc.LOGDEBUG)

                # Wait for 1s before the next call
                time.sleep(1)
        else:
            # Other HTTP error - FATAL, do not retry
            xbmc.log(
                f"FATAL: Could not get URL: {url} - HTTP Status Code {status_code}",
                xbmc.LOGDEBUG)
            break

        current_try = current_try + 1

    return request


def get_nhk_website_url(path):
    """ Return a full URL from the partial URLs in the JSON results """
    nhk_website = "https://www3.nhk.or.jp"
    return nhk_website + path
