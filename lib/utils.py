from datetime import datetime, timedelta

import requests
import requests_cache
import xbmc
import xbmcaddon
from pytz import timezone
from tzlocal import get_localzone


# Get Plug-In path
ADDON = xbmcaddon.Addon()
plugin_path = ADDON.getAddonInfo('path')
if (len(plugin_path)>0):
    # Running within Kodi - use that path
    db_name = '{0}/nhk_world_cache'.format(plugin_path)
else:
    # Running under unit test
    db_name ='nhk_world_cache'

# Enable cache for requests
requests_cache.install_cache(db_name, backend='sqlite', expire_after=300)

# Instantiate request session
s = requests.Session()
api_key = 'EJfK8jdS57GqlupFgAfAAwr573q01y6k'
request_params = {'apikey': api_key}
s.params = request_params

# Get JSON object from a URL with improved error handling


def get_json(url, cached = True):
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


# Get a URL with automatic retries - NHK sometimes have intermittent problems


def get_url(url, cached = True):
    # maximum number of retries
    max_retries = 3
    current_try = 1
    while (current_try <= max_retries):
        # Only add the API key for API Calls

        # Use cached or non-cached result
        if (cached):
            # Use session cache
            r = s.get(url)
        else:
            with s.cache_disabled():
                # Don't use session cache
                r = s.get(url)

        # Make an API Call
        xbmc.log('Making API Call {0} ({1} of {2})'.format(
            r.url, current_try, max_retries))

        if (r.status_code == 200):
            # Call was successfull
            xbmc.log(
                'Successfully fetched URL/API: {0} - Status {1} - Retrieved from cache {2}'.format(
                    r.url, r.status_code, r.from_cache))
            return (r)
        else:
            if (current_try == max_retries):
                # Max retries reached - still could not get url
                # Failure - no way to handle - probably an issue
                # with the NHK Website
                # Raise exception
                xbmc.log(
                    'Could not get URL {0} - HTTP Status Code {1} - Retries {2}'
                    .format(r.url, r.status_code, max_retries), xbmc.LOGFATAL)
                r.raise_for_status()
            else:
                # Wait for n seconds and then try again
                xbmc.log(
                    'Failure fetching URL: {0} with Status {1})'.format(
                        r.url, r.status_code), xbmc.LOGWARNING)
                current_try = +1


# Return a full URL from the partial URLs in the JSON results


def get_NHK_website_url(path):
    nhk_website = 'https://www3.nhk.or.jp'
    return nhk_website + path


# Convert Timezone from UTC to local TZ


def to_local_time(UTC_timestamp):
    # Convert from JST to local timezone
    UTC_tz = timezone('Etc/UTC')
    local_tz = get_localzone()

    # Parse it as UTC
    UTC_datetime = UTC_tz.localize(datetime.fromtimestamp(UTC_timestamp))
    UTC_datetime = UTC_datetime - timedelta(hours=1)

    # Convert to local time
    local_datetime = UTC_datetime.astimezone(local_tz)

    # Localize time again to get the correct TZINFO
    dt = local_tz.localize(
        datetime(local_datetime.year, local_datetime.month, local_datetime.day,
                 local_datetime.hour, local_datetime.minute,
                 local_datetime.second))
    return (dt)


# Construct an epsidode name from the title and the subtitle


def get_episode_name(title, subtitle):
    if len(subtitle) == 0:
        episode_name = u'{0}'.format(title)
    else:
        episode_name = u'{0} - {1}'.format(title, subtitle)
    return (episode_name)
