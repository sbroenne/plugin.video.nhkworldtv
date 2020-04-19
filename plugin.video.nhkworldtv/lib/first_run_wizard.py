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

    abort_wizard = dialog.yesno('1 of 4: Set-up Wizard - Welcome',
                                delimiter.join(lines),
                                nolabel='Yes, continue set-up',
                                yeslabel='No, I am good')

    if (abort_wizard):
        ADDON.setSettingBool('run_wizard', False)
        return (False)

    lines = []
    lines.append(
        'This plug-in can use a Microsoft Azure hosted cache service to speed-up video play-back'
    )
    lines.append('This is enabled by default.')
    lines.append('Do you want disable this setting?')
    disable_azure_cache = dialog.yesno('2 of 4: Set-up Wizard - {0}'.format(
        get_string(30002)),
                                       delimiter.join(lines),
                                       nolabel='No, leave it on',
                                       yeslabel='Yes, disable it')

    if (disable_azure_cache):
        ADDON.setSettingBool('use_backend', False)

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
        '3 of 4: Set-up Wizard - Auto Kodi view modes',
        delimiter.join(lines),
        nolabel='No',
        yeslabel='Yes, please auto-set')

    if (enable_view_mode):
        ADDON.setSettingBool('set_view_mode', True)

    lines = []
    lines.append(
        'NHK provides streams in LQ, SD, 720P in medium and Full-HD (1080P) in very hiqh quality'
    )
    lines.append(
        'By default the plug-in will play 1080P. If you encounter buffering issues, you can select a lower quality.'
    )
    lines.append(
        'You can do this by changing the Kodi "Internet bandwidth limitations" system-setting'
    )
    lines.append(
        'You find this setting by going to: "(Gears icons) - System - Settings - Internet access - Internet connection bandwidth limitation'
    )
    lines.append(
        'Everything over "1536 kbps" will disable 1080P (1080P requires at least 10.000 kbps).'
    )
    lines.append(
        'Default setting is "off" (play 1080P where available). This is a Kodi-wide system setting.'
    )
    lines.append(
        'The wizard has finished and will close now. Enjoy NHK World TV!')

    complete = dialog.ok('4 of 4: Set-up Wizard - Buffering problems',
                         delimiter.join(lines))

    if (complete):
        ADDON.setSettingBool('run_wizard', False)

    return (True)
