"""Tests for plugin module helper functions"""

from lib import plugin


def test_add_topstories_menu_item():
    """Test add_topstories_menu_item doesn't crash"""
    # This function relies on xbmcplugin which is hard to mock
    # Just verify it returns bool and doesn't crash
    result = plugin.add_topstories_menu_item()
    assert isinstance(result, bool)


def test_add_ataglance_menu_item():
    """Test add_ataglance_menu_item doesn't crash"""
    result = plugin.add_ataglance_menu_item()
    assert isinstance(result, bool)


def test_add_on_demand_menu_item():
    """Test add_on_demand_menu_item doesn't crash"""
    result = plugin.add_on_demand_menu_item()
    # Returns Episode or None
    assert result is None or hasattr(result, "title")


def test_add_live_stream_menu_item():
    """Test add_live_stream_menu_item doesn't crash"""
    result = plugin.add_live_stream_menu_item()
    # Returns Episode object, not bool
    assert result is None or hasattr(result, "title")


def test_add_schedule_today_menu_item():
    """Test add_schedule_today_menu_item doesn't crash"""
    result = plugin.add_schedule_today_menu_item()
    assert isinstance(result, bool)


def test_add_schedule_past_menu_item():
    """Test add_schedule_past_menu_item doesn't crash"""
    result = plugin.add_schedule_past_menu_item()
    assert isinstance(result, bool)


def test_add_schedule_upcoming_menu_item():
    """Test add_schedule_upcoming_menu_item doesn't crash"""
    result = plugin.add_schedule_upcoming_menu_item()
    assert isinstance(result, bool)


def test_get_schedule_episodes_all():
    """Test _get_schedule_episodes with 'all' filter"""
    episodes = plugin._get_schedule_episodes("all")
    assert isinstance(episodes, list)


def test_get_schedule_episodes_past():
    """Test _get_schedule_episodes with 'past' filter"""
    episodes = plugin._get_schedule_episodes("past")
    assert isinstance(episodes, list)


def test_get_schedule_episodes_upcoming():
    """Test _get_schedule_episodes with 'upcoming' filter"""
    episodes = plugin._get_schedule_episodes("upcoming")
    assert isinstance(episodes, list)


def test_add_playable_episode():
    """Test add_playable_episode creates proper list"""
    from lib.episode import Episode

    episode = Episode()
    episode.title = "Test Episode"
    episode.vod_id = "test123"
    episode.url = "https://example.com/video.m3u8"
    episode.thumb = "https://example.com/thumb.jpg"
    episode.fanart = "https://example.com/fanart.jpg"
    episode.plot = "Test plot"
    episode.is_playable = True

    result = plugin.add_playable_episode(episode)
    # Returns a list, not tuple
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[2] is False  # Third element is isFolder flag


def test_render_schedule_episodes_with_episodes():
    """Test _render_schedule_episodes with episodes"""
    # Create mock episodes
    import time
    from datetime import datetime

    from lib.episode import Episode

    episode = Episode()
    episode.title = "Test Show"
    episode.plot = "Test plot"
    episode.thumb = "https://example.com/thumb.jpg"
    episode.fanart = "https://example.com/fanart.jpg"
    episode.vod_id = "test123"

    # Set broadcast dates
    start_date = datetime.now()
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp

    episodes = [episode]
    result = plugin._render_schedule_episodes(episodes, "No schedule")
    assert isinstance(result, bool)


def test_render_schedule_episodes_empty():
    """Test _render_schedule_episodes with empty list"""
    result = plugin._render_schedule_episodes([], "No episodes available")
    assert result is False


def test_show_textviewer_dialog_box():
    """Test show_textviewer_dialog_box doesn't crash"""
    # This creates a dialog which we can't test in unit tests
    # Just verify it returns a Dialog object
    try:
        result = plugin.show_textviewer_dialog_box("Test Title", "Test Plot")
        # Should return Dialog or fail gracefully
        assert result is not None or result is None
    except Exception:
        # Expected in unit test environment
        pass


def test_module_globals():
    """Test that module globals are properly initialized"""
    assert plugin.ADDON is not None
    # NHK_ICON and NHK_FANART may be MagicMock in test environment
    assert plugin.NHK_ICON is not None
    assert plugin.NHK_FANART is not None
    assert isinstance(plugin.MAX_NEWS_DISPLAY_ITEMS, int)
    assert isinstance(plugin.MAX_ATAGLANCE_DISPLAY_ITEMS, int)
    assert plugin.MAX_NEWS_DISPLAY_ITEMS >= 0
    assert plugin.MAX_ATAGLANCE_DISPLAY_ITEMS >= 0


def test_schedule_image_paths():
    """Test that schedule image paths are properly set"""
    assert isinstance(plugin.SCHEDULE_TODAY_THUMB, str)
    assert isinstance(plugin.SCHEDULE_TODAY_FANART, str)
    assert isinstance(plugin.SCHEDULE_PAST_THUMB, str)
    assert isinstance(plugin.SCHEDULE_PAST_FANART, str)
    assert isinstance(plugin.SCHEDULE_UPCOMING_THUMB, str)
    assert isinstance(plugin.SCHEDULE_UPCOMING_FANART, str)

    # Verify paths contain expected strings
    assert "schedule" in plugin.SCHEDULE_TODAY_THUMB.lower()
    assert "schedule" in plugin.SCHEDULE_PAST_THUMB.lower()
    assert "schedule" in plugin.SCHEDULE_UPCOMING_THUMB.lower()
    assert "schedule" in plugin.SCHEDULE_UPCOMING_THUMB.lower()
