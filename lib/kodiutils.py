# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import sys
import logging

# read settings
ADDON = xbmcaddon.Addon()

logger = logging.getLogger(__name__)


def notification(header, message, time=5000, icon=ADDON.getAddonInfo('icon'), sound=True):
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
    return ADDON.getLocalizedString(string_id).encode('utf-8', 'ignore')

# Set the Kodi View Mode
def set_view_mode(view_mode_id):
    if (get_setting_as_bool('set_view_mode')):
        # Change view mode 
        logger.debug('Switching to View Mode: {0}'.format(view_mode_id))
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    else:
        # Setting was disabled - do not change view mode
        logger.debug('SETTING NOT ENABLED: View Mode mot changed - requested view mode: {0}'.format(view_mode_id))

# Set the Kodi Sort Direction
def set_sort_direction(sort_direction):
    # Sort Order can be Ascending or Descending
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    logger.debug('Current sort order: {0}'.format(current_sort_direction))
    #FIXME: Not working right now since Kodi always returns Ascending - need to investigate
    """   if (current_sort_direction <> sort_direction):
        xbmc.executebuiltin('Container.SetSortDirection')
        logger.debug('Toggling sort direction from {0} to {1}'.format(current_sort_direction, sort_direction)) """