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


def get_string(string_id):
    localized_string = ADDON.getLocalizedString(string_id)
    if len(localized_string) > 0:
        return localized_string
    else:
        # Running under unit test - return a unit test string
        returnString = 'UNIT TEST LOCALIZED STRING {0}'.format(string_id)
        return returnString


def get_video_info(use_720p):
    """ Returns a list item video info

    Args:
        use720p ([boolean]): Use 720P or 1080p.

    Returns:
        [dict]: A video_info dict
    """
    if (use_720p):
        return (get_720_HD_video_info())
    else:
        return (get_1080_HD_video_info())


# Returns a Full-HD (1080p) video info array
def get_1080_HD_video_info():
    video_info = {'aspect': '1.78', 'width': '1920', 'height': '1080'}
    return (video_info)


# Returns a HD (720p) video info array
def get_720_HD_video_info():
    video_info = {'aspect': '1.78', 'width': '1280', 'height': '720'}
    return (video_info)


# Returns a SD video info array
def get_SD_video_info():
    video_info = {'aspect': '1.82', 'width': '640', 'height': '368'}
    return (video_info)


def set_video_directory_information(plugin_handle,
                                    view_mode,
                                    sort_method,
                                    content_type='videos'):
    """Sets the metadate like VIEW_MODE and SORT_METHOD on the
    current Kodi directory

    Arguments:
        plugin_handle {int} -- Plugin handle
        view_mode {int} -- e.g kodiutils.VIEW_MODE_INFOWALL
        sort_method {int} -- xbmcplugin.SORT_METHOD_TITLE
        content_type {unicode} -- videos, episodes, tvshows, etc.
    """
    # Debug logging
    current_viewmode = xbmc.getInfoLabel('Container.ViewMode')
    current_sort_method = xbmc.getInfoLabel('Container.SortMethod')
    xbmc.log('Current view mode/sort method: {0}/{1}'.format(
        current_viewmode, current_sort_method))
    xbmc.log('Requested view mode/sort method: {0}/{1}'.format(
        VIEW_MODES_REVERSE[view_mode], sort_method))

    # Set sort method
    xbmcplugin.addSortMethod(plugin_handle, sort_method)

    # Setting view mode - needs to be enabled in settings
    if (ADDON.getSettingBool('set_view_mode')):
        # Change view mode
        xbmc.log('Switching to View Mode: {0}'.format(
            VIEW_MODES_REVERSE[view_mode]))
        # Set the content
        if (view_mode != VIEW_MODE_WIDELIST):
            # Do not set the content typ for WideList
            xbmcplugin.setContent(plugin_handle, content_type)
        xbmc.executebuiltin('Container.SetViewMode({0})'.format(view_mode))
    else:
        # Setting was disabled - do not change view mode
        xbmc.log('SETTING NOT ENABLED: View Mode mot changed\
                 - requested view mode: {0}'.format(
            VIEW_MODES_REVERSE[view_mode]))
        if (content_type != 'videos'):
            # Set the content to a more specific content type than videos
            xbmcplugin.setContent(plugin_handle, content_type)

    # End of Directory
    xbmcplugin.endOfDirectory(plugin_handle, succeeded=True, cacheToDisc=False)


def get_episodelist_title(title, total_episodes):
    """Returns a formated episode list title
    Arguments:
        title {unicode} -- episode list title
        total_episodes {unicode} -- number of episodes
    Returns:
        {unicode} -- Journeys in Japan - 2 Episodes
    """

    if (total_episodes == 1):
        episodelist_title = get_string(30090).format(title, total_episodes)
    else:
        episodelist_title = get_string(30091).format(title, total_episodes)
    return (episodelist_title)
