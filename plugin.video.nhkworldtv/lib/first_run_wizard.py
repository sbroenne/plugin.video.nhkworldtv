from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from kodi_six import xbmc, xbmcgui, xbmcaddon
from . import kodiutils, utils
ADDON = xbmcaddon.Addon()


def show_wizard():
    """Shows the first run wizard
    """

    if (not ADDON.getSettingBool('run_wizard')):
        return (False)

    # Step 1
    xbmc.log("Starting Set-up Wizard")
    dialog = xbmcgui.Dialog()

    abort_wizard = dialog.yesno(kodiutils.get_string(30070),
                                kodiutils.get_string(30071),
                                nolabel=kodiutils.get_string(30072),
                                yeslabel=kodiutils.get_string(30073))

    if (utils.UNIT_TEST is False):
        # Don't abort if under unit test
        if (abort_wizard):
            ADDON.setSettingBool('run_wizard', False)
            return (False)

    # Step 2

    enable_view_mode = dialog.yesno(kodiutils.get_string(30074),
                                    kodiutils.get_string(30075),
                                    nolabel=kodiutils.get_string(30076),
                                    yeslabel=kodiutils.get_string(30077))

    if (enable_view_mode):
        ADDON.setSettingBool('set_view_mode', True)

    complete = dialog.ok(kodiutils.get_string(30078),
                         kodiutils.get_string(30079))

    if (complete):
        ADDON.setSettingBool('run_wizard', False)

    return (True)
