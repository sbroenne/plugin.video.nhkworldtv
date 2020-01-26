import urllib
import xbmc
import requests

# Loglevel will be overriden at runtime
LOGLEVEL = xbmc.LOGDEBUG

# Helper Functions
# Get JSON object from a URL with improved error handling
def get_json(url):
    r = get_url(url, True)
    try:
        result = r.json()
        return(result)
    except:
        r.raise_for_status()

 # Get a URL with automatic retries - NHK sometimes have intermittent problems
def get_url(url, withAPIKey = False):
    # maximum number of retries
    max_retries = 3
    current_try = 1
    while (current_try <= max_retries):
        # Only add the API key for API Calls
        if (withAPIKey):
            apikey = 'EJfK8jdS57GqlupFgAfAAwr573q01y6k'
            request_params = {'apikey': apikey}
            r = requests.get(url, request_params)
            xbmc.log('Making API Call {0} ({1} of {2})'.format(r.url, current_try, max_retries), level=LOGLEVEL)
        else:
            r = requests.get(url)
            xbmc.log('Fetching URL {0} ({1} of {2})'.format(r.url, current_try, max_retries), level=LOGLEVEL)
        if (r.status_code == 200):
            xbmc.log('Successfully fetched URL/API: {0} with Status {1}'.format(r.url, r.status_code), level=LOGLEVEL)
            return(r)
        else:
            if (current_try == max_retries):
                xbmc.log('Could not get URL {0} - Last HTTP Status Code {1} - Retries {2}'.format(r.url, r.status_code, max_retries), xbmc.LOGFATAL)
            else:
                # Wait for n seconds
                xbmc.log('Failure fetching URL: {0} with Status {1}'.format(r.url, r.status_code), level=LOGLEVEL)
                current_try = +1


# Return a full URL from the partial URLs in the JSON results
def get_NHK_website_url(url):
    nhk_website = 'https://www3.nhk.or.jp/'
    return nhk_website[:-1]+url
    