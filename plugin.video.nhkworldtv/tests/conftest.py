"""
Pytest configuration and fixtures for plugin.video.nhkworldtv tests.

This module sets up mocks for Kodi modules that are not available
in the test environment.
"""

import sys
from unittest.mock import MagicMock

# Mock all Kodi modules before any test imports them
sys.modules["xbmc"] = MagicMock()
sys.modules["xbmcgui"] = MagicMock()
sys.modules["xbmcplugin"] = MagicMock()
sys.modules["xbmcaddon"] = MagicMock()
sys.modules["xbmcvfs"] = MagicMock()
sys.modules["routing"] = MagicMock()
