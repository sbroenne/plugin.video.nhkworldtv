# NHK World TV
# WIll be called by KODI
# File is not cached so main logic can is in lib/mayn.pi


# import python libraries
import xbmc
import xbmcaddon
import sys
import urlparse
from libs import main

# Start of main program loop
LOGLEVEL = xbmc.LOGDEBUG

# ID of the plugin
PLUGIN_ID = 'plugin.video.nhkworldtv'

# Get master data
addon = xbmcaddon.Addon(PLUGIN_ID)
nhk_icon = addon.getAddonInfo('icon')  # icon.png in addon directory
addon_name = addon.getAddonInfo('name')

# Main logic

# Plugin base URL and add-on handle
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

xbmc.log('Plugin {0} with handle {1} starting with {2} arguments'.format(addon_name, addon_handle,
    len(sys.argv)), level=xbmc.LOGNOTICE)
xbmc.log('Base Url: {0}'.format(base_url), level=LOGLEVEL)

# Query excution mode and url
args = urlparse.parse_qs(sys.argv[2][1:])
# urlparse.parse_qs returns the dictionary values as a list - so need to always get the first [0] element
mode = args.get('mode', None)[0]
xbmc.log('Exectution mode: {0}'.format(mode), level=LOGLEVEL)
url = args.get('url', None)[0]
xbmc.log('Target Url: {0}'.format(url), level=LOGLEVEL)

# Excute main logic loop
main.run(url, mode, args)