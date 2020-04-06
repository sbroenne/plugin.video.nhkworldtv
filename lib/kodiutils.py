# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)
from kodi_six import xbmc, xbmcaddon, xbmcplugin

# read settings
ADDON = xbmcaddon.Addon()

# View Modes from the default Estuary skin
VIEW_MODE_INFOWALL = 54
VIEW_MODE_WALL = 500
VIEW_MODE_WIDELIST = 55

# Reverse values to handle feedback from Kodi GUI
VIEW_MODES_REVERSE = {
    VIEW_MODE_INFOWALL: 'InfoWall',
    VIEW_MODE_WIDELIST: 'WideList',
    VIEW_MODE_WALL: 'Wall'
}
SORT_METHODS_REVERSE = {
    xbmcplugin.SORT_METHOD_DATE: 'Date',
    xbmcplugin.SORT_METHOD_NONE: 'None',
    xbmcplugin.SORT_METHOD_TITLE: 'Title'
}


def get_string(string_id):
    # FIXME: Force returnString to be Unicode - simple .encode did not work!
    localized_string = ADDON.getLocalizedString(string_id).encode(
        'utf-8', 'ignore')
    if len(localized_string) > 0:
        returnString = '{0}'.format(localized_string)
    else:
        # Running under unit test - return a unit test string
        returnString = 'UNIT TEST LOCALIZED STRING {0}'.format(string_id)
    return returnString


# Set the Kodi View Mode
def set_view_mode(view_mode_id):
    if (ADDON.getSettingBool('set_view_mode')):
        # Change view mode
        xbmc.log('Switching to View Mode: {0}'.format(
            VIEW_MODES_REVERSE[view_mode_id]))
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    else:
        # Setting was disabled - do not change view mode
        xbmc.log('SETTING NOT ENABLED: View Mode mot changed\
                 - requested view mode: {0}'.format(
            VIEW_MODES_REVERSE[view_mode_id]))


# Returns a Full-HD (1080p) video info array
def get_1080_HD_video_info():
    video_info = {'aspect': '1.78', 'width': '1920', 'height': '1080'}
    return (video_info)


# Returns a SD video info array
def get_SD_video_info():
    video_info = {'aspect': '1.82', 'width': '640', 'height': '368'}
    return (video_info)


# Sets the metadatalike VIEW_MODE and SORT_METHOD on the current Kodi directory
def set_video_directory_information(plugin_handle, view_mode, sort_method,
                                    sort_direction):
    """ Sets the metadate like VIEW_MODE and SORT_METHOD on the c
    urrent Kodi directory
    sort_direction can be either Ascending or Descending
    """

    # This plugin displays videos
    # Important to set because otherwise you cannot chang the view mode
    # to InfoWall, etc.
    xbmcplugin.setContent(plugin_handle, 'videos')

    # Debug logging
    current_viewmode = xbmc.getInfoLabel('Container.ViewMode')
    current_sort_method = xbmc.getInfoLabel('Container.SortMethod')
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    xbmc.log('Current view mode/sort method/order: {0}/{1}/{2}'.format(
        current_viewmode, current_sort_method, current_sort_direction))
    xbmc.log('Requested view mode/sort method/direction: {0}/{1}/{2}'.format(
        VIEW_MODES_REVERSE[view_mode], SORT_METHODS_REVERSE[sort_method],
        sort_direction))

    # Set the view mode (e.g. InfoWall)
    set_view_mode(view_mode)

    # Set sorg method
    if (sort_method != 'None'):
        xbmcplugin.addSortMethod(plugin_handle, sort_method)

    # Sort Order can be Ascending, Descending or None
    #
    # FIXME: This seems to be broken in Kodi 18.6 - current sort order always
    # returns Ascending - even if it is descendingg
    # t looks like Kodi always return from values from the
    # parent container and not the the current container
    # that we are creating here
    # Not sure if this is by design
    """  if sort_direction != 'None':
        if (current_sort_direction != sort_direction):
            xbmc.log('Toggling sort direction from {0} to {1}'.format(
                current_sort_direction, sort_direction))
            xbmc.executebuiltin('Container.SetSortDirection') """

    xbmcplugin.endOfDirectory(plugin_handle, succeeded=True, cacheToDisc=False)

    # Debug logging
    current_viewmode = xbmc.getInfoLabel('Container.Viewmode')
    current_sort_method = xbmc.getInfoLabel('Container.SortMethod')
    current_sort_direction = xbmc.getInfoLabel('Container.SortOrder')
    xbmc.log('New view mode/sort method/order: {0}/{1}/{2}'.format(
        current_viewmode, current_sort_method, current_sort_direction))
