# -*- coding: utf-8 -*-

from lib import kodilogging
from lib import plugin

import logging
import xbmcaddon

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
kodilogging.config()

plugin.run()


