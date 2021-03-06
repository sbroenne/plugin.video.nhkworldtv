# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from kodi_six import xbmc, xbmcgui
from .kodiutils import get_string


def show_wizard(ADDON):
    """Shows the first run wizard
    """

    if (not ADDON.getSettingBool('run_wizard')):
        return (False)

    xbmc.log("Starting Set-up Wizard")
    dialog = xbmcgui.Dialog()

    delimiter = '\n\n'
    lines = []
    lines.append('NHK World TV comes with a set of configurable options.')
    lines.append('You can always change them in the addon-settings later.')
    lines.append(
        'For the best user experience I would suggest to set-up some settings now.'
    )

    abort_wizard = dialog.yesno('1 of 3: Set-up Wizard - Welcome',
                                delimiter.join(lines),
                                nolabel='Yes, continue set-up',
                                yeslabel='No, I am good')

    if (abort_wizard):
        ADDON.setSettingBool('run_wizard', False)
        return (False)

    lines = []
    lines.append(
        'The plug-in can automatically set view modes (e.g. InfoWall) that best match the type of NHK content',
    )
    lines.append(
        'This is disabled by default because it is a Kodi recommendation not to auto-set this.'
    )
    lines.append(
        'If you use the default Kodi skin (Estuary) I would recommend to auto-set view modes - this will give you the best user experience.'
    )
    lines.append('Do you want enable auto-setting of view modes?')

    enable_view_mode = dialog.yesno(
        '2 of 3: Set-up Wizard - Auto Kodi view modes',
        delimiter.join(lines),
        nolabel='No',
        yeslabel='Yes, please auto-set')

    if (enable_view_mode):
        ADDON.setSettingBool('set_view_mode', True)

    lines = []
    lines.append(
        'NHK provides streams in 720P in medium and Full-HD (1080P) in very hiqh quality.'
    )
    lines.append(
        'By default the plug-in will play 1080P.'
    )
    lines.append(
        'If you encounter buffering issues, you can select a lower quality by changing the "Use 720P instead of 1080P" addon-setting.'
    )
    lines.append(
        'The wizard has finished and will close now. Enjoy NHK World TV!')

    complete = dialog.ok('3 of 3: Set-up Wizard - 1080P',
                         delimiter.join(lines))

    if (complete):
        ADDON.setSettingBool('run_wizard', False)

    return (True)
