# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

# read settings
ADDON = xbmcaddon.Addon()


def notification(header,
                 message,
                 time=5000,
                 icon=ADDON.getAddonInfo('icon'),
                 sound=True):
    xbmcgui.Dialog().notification(header, message, icon, time, sound)


def show_settings():
    ADDON.openSettings()


def get_setting(setting):
    return ADDON.getSetting(setting).strip().decode('utf-8')


def set_setting(setting, value):
    ADDON.setSetting(setting, str(value))


def get_setting_as_bool(setting):
    return get_setting(setting).lower() == "true"


def get_setting_as_float(setting):
    try:
        return float(get_setting(setting))
    except ValueError:
        return 0


def get_setting_as_int(setting):
    try:
        return int(get_setting_as_float(setting))
    except ValueError:
        return 0


def get_string(string_id):
    # FIXME: Force returnString to be Unicode - simple .encode did not work!
    localized_string = ADDON.getLocalizedString(string_id).encode('utf-8', 'ignore')
    if len(localized_string)>0:
        returnString = u'{0}'.format(localized_string)
    else:
        # Running under unit test - return a unit test string
        returnString = u'UNIT TEST LOCALIZED STRING {0}'.format(string_id)
    return returnString


# Set the Kodi View Mode
def set_view_mode(view_mode_id):
    if (get_setting_as_bool('set_view_mode')):
        # Change view mode
        xbmc.log('Switching to View Mode: {0}'.format(view_mode_id))
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    else:
        # Setting was disabled - do not change view mode
        xbmc.log(
            'SETTING NOT ENABLED: View Mode mot changed - requested view mode: {0}'
            .format(view_mode_id))


# Set the Kodi Sort Direction
def set_sort_direction(sort_direction):
    xbmc.log('Requested sort direction: {0}'.format(sort_direction))
    # Sort Order can be Ascending or Descending
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    xbmc.log('Current sort order: {0}'.format(current_sort_direction))
    #
    # FIXME: This seems to be broken in Kodi 18.6 - current sort order always returns Ascending even if it is descendingg
    #
    #if (current_sort_direction <> sort_direction):
    #    xbmc.executebuiltin('Container.SetSortDirection')
    #    xbmc.log('Toggling sort direction from {0} to {1}'.format(current_sort_direction, sort_direction))


# Returns a Full-HD (1080p) video info array
def get_1080_HD_video_info():
    video_info = {'aspect': '1.78', 'width': '1920', 'height': '1080'}
    return (video_info)


# Returns a SD video info array
def get_SD_video_info():
    video_info = {'aspect': '1.78', 'width': '640', 'height': '360'}
    return (video_info)
