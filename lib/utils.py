import xbmcaddon
import requests
import logging
import kodilogging
from kodiutils import get_setting_as_bool
from nhk_api import rest_url
from datetime import datetime, timedelta
from pytz import timezone
from tzlocal import get_localzone

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

# Instaniate sessions
s = requests.Session()
api_key = rest_url['api_key']
request_params = {'apikey': api_key}
s.params=request_params

# Helper Functionspi
# Get JSON object from a URL with improved error handling
def get_json(url):
    r = get_url(url)
    try:
        result = r.json()
        logger.debug('Successfully loaded JSON from API: {0} with Status {1}'.format(r.url, r.status_code))
        return(result)
    except:
        # Failure - no way to handle - probably an issue with the NHK Website - raise exception
        r.raise_for_status()

 # Get a URL with automatic retries - NHK sometimes have intermittent problems
def get_url(url):
    # maximum number of retries
    max_retries = 3
    current_try = 1
    while (current_try <= max_retries):
        # Only add the API key for API Calls
        r = s.get(url)
        # Make an API Call
        logger.debug('Making API Call {0} ({1} of {2})'.format(r.url, current_try, max_retries))
        
        if (r.status_code == 200):
            # Call was successfull
            logger.debug('Successfully fetched URL/API: {0} with Status {1}'.format(r.url, r.status_code))
            return(r)
        else:
            if (current_try == max_retries):
                # Max retries reached - still could not get url
                # Failure - no way to handle - probably an issue with the NHK Website - raise exception
                logger.fatal('Could not get URL {0} - Last HTTP Status Code {1} - Retries {2}'.format(r.url, r.status_code, max_retries))
                r.raise_for_status()
            else:
                # Wait for n seconds and then try again
                logger.warning('Failure fetching URL: {0} with Status {1})'.format(r.url, r.status_code))
                current_try = +1


# Return a full URL from the partial URLs in the JSON results
def get_NHK_website_url(path):
    nhk_website = 'https://www3.nhk.or.jp'
    return nhk_website+path


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
    dt = local_tz.localize(datetime(local_datetime.year, local_datetime.month, local_datetime.day, local_datetime.hour, local_datetime.minute, local_datetime.second))
    return (dt)