import urllib
import xbmc
import xbmcgui
import xbmcaddon
import requests
import logging
import kodilogging

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

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
            logger.debug('Making API Call {0} ({1} of {2})'.format(r.url, current_try, max_retries))
        else:
            r = requests.get(url)
            logger.debug('Fetching URL {0} ({1} of {2})'.format(r.url, current_try, max_retries))
        if (r.status_code == 200):
            logger.debug('Successfully fetched URL/API: {0} with Status {1}'.format(r.url, r.status_code))
            return(r)
        else:
            if (current_try == max_retries):
                logger.debug('Could not get URL {0} - Last HTTP Status Code {1} - Retries {2}'.format(r.url, r.status_code, max_retries))
            else:
                # Wait for n seconds
                logger.debug('Failure fetching URL: {0} with Status {1}'.format(r.url, r.status_code))
                current_try = +1


# Return a full URL from the partial URLs in the JSON results
def get_NHK_website_url(url):
    nhk_website = 'https://www3.nhk.or.jp'
    return nhk_website+url


# Set the Kodi View Mode
def set_view_mode(view_mode_id):
    logger.debug('Switching to View Mode {0}'.format(view_mode_id))
    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
        

# Set the Kodi Sort Direction
def set_sort_direction(sort_direction):
    # Sort Order can be Ascending or Descending
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    logger.debug('Current sort order: {0}'.format(current_sort_direction))
    #FIXME: Not working right now since Kodi always returns Ascending - need to investigate
    """   if (current_sort_direction <> sort_direction):
        xbmc.executebuiltin('Container.SetSortDirection')
        logger.debug('Toggling sort direction from {0} to {1}'.format(current_sort_direction, sort_direction)) """
