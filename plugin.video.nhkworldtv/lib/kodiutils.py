"""
Kodi specific utils
"""
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

# read settings
ADDON = xbmcaddon.Addon()


def get_string(string_id):
    """Get a localized string"""
    localized_string = ADDON.getLocalizedString(string_id)

    if len(localized_string) > 0:
        return_string = localized_string
    else:
        # Running under unit test - return a unit test string
        return_string = f"UNIT TEST LOCALIZED STRING {string_id}"

    return return_string


def show_notification(title, message, time_ms=5000):
    """Show a Kodi notification to the user
    
    Args:
        title (str): Notification title
        message (str): Notification message
        time_ms (int): Display time in milliseconds (default 5000)
    """
    try:
        xbmcgui.Dialog().notification(
            title, message, xbmcgui.NOTIFICATION_INFO, time_ms
        )
    except Exception:
        # Fallback to log if notification fails (e.g., during unit tests)
        xbmc.log(f"Notification: {title} - {message}", xbmc.LOGINFO)


def get_video_info():
    """Returns a list item video info for HD streams

    Returns:
        [dict]: A video_info dict
    """
    video_info = {"aspect": "1.78", "width": "1280", "height": "720"}
    return video_info


def get_sd_video_info():
    """
    Returns a SD video info array
    """
    video_info = {"aspect": "1.82", "width": "640", "height": "368"}
    return video_info


def set_video_directory_information(
    plugin_handle, sort_method, content_type="videos"
):
    """Sets the metadata like SORT_METHOD on the
    current Kodi directory

    Arguments:
        plugin_handle {int} -- Plugin handle
        sort_method {int} -- xbmcplugin.SORT_METHOD_TITLE
        content_type {str} -- videos, episodes, tvshows, etc.
    """
    # Debug logging
    current_sort_method = xbmc.getInfoLabel("Container.SortMethod")
    xbmc.log(f"Current sort method: {current_sort_method}")
    xbmc.log(f"Requested sort method: {sort_method}")

    # Set sort method
    xbmcplugin.addSortMethod(plugin_handle, sort_method)
    if content_type != "videos":
        # Set the content to a more specific content type than videos
        xbmcplugin.setContent(plugin_handle, content_type)

    # End of Directory
    xbmcplugin.endOfDirectory(plugin_handle, succeeded=True, cacheToDisc=False)


def get_episodelist_title(title, total_episodes):
    """Returns a formatted episode list title
    Arguments:
        title {unicode} -- episode list title
        total_episodes {unicode} -- number of episodes
    Returns:
        {unicode} -- Journeys in Japan - 2 Episodes
    """

    if total_episodes == 1:
        episodelist_title = get_string(30090).format(title, total_episodes)
    else:
        episodelist_title = get_string(30091).format(title, total_episodes)
    return episodelist_title
