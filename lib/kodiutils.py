# -*- coding: utf-8 -*-

import logging

import xbmc
import xbmcaddon
import xbmcgui

# read settings
ADDON = xbmcaddon.Addon()
logger = logging.getLogger(__name__)


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
    returnString = u'{0}'.format(
        ADDON.getLocalizedString(string_id).encode('utf-8', 'ignore'))
    return returnString


# Set the Kodi View Mode
def set_view_mode(view_mode_id):
    if (get_setting_as_bool('set_view_mode')):
        # Change view mode
        logger.debug('Switching to View Mode: {0}'.format(view_mode_id))
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    else:
        # Setting was disabled - do not change view mode
        logger.debug(
            'SETTING NOT ENABLED: View Mode mot changed - requested view mode: {0}'
            .format(view_mode_id))


# Set the Kodi Sort Direction
def set_sort_direction(sort_direction):
    # Sort Order can be Ascending or Descending
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    logger.debug('Current sort order: {0}'.format(current_sort_direction))
    #
    # FIXME: Not working right now since Kodi always returns Ascending
    # need to investigate
    #  if (current_sort_direction <> sort_direction):
    #    xbmc.executebuiltin('Container.SetSortDirection')
    #    logger.debug('Toggling sort direction from {0} to {1}'
    # .format(current_sort_direction, sort_direction))


# Returns a Full-HD (1080p) video info array
def get_1080_HD_video_info():
    video_info = {'aspect': '1.78', 'width': '1920', 'height': '1080'}
    return (video_info)


# Returns a SD video info array
def get_SD_video_info():
    video_info = {'aspect': '1.78', 'width': '640', 'height': '360'}
    return (video_info)
