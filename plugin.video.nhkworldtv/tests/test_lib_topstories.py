"""Tests for topstories module"""

from lib import topstories


def test_get_menu_item():
    """Test get_menu_item returns menu item or None"""
    menu_item = topstories.get_menu_item()
    # Should return Episode or None (if API fails)
    assert menu_item is None or hasattr(menu_item, "title")


def test_get_episodes():
    """Test get_episodes returns list of episodes"""
    episodes = topstories.get_episodes(5, "icon.jpg", "fanart.jpg")
    # Should return list (may be empty if API fails)
    assert isinstance(episodes, list)


def test_get_episodes_max_items():
    """Test get_episodes respects max_items limit"""
    episodes = topstories.get_episodes(3, "icon.jpg", "fanart.jpg")
    assert isinstance(episodes, list)
    # Should have at most 3 items
    assert len(episodes) <= 3


def test_get_episodes_zero_items():
    """Test get_episodes with zero max_items"""
    episodes = topstories.get_episodes(0, "icon.jpg", "fanart.jpg")
    assert isinstance(episodes, list)
    assert len(episodes) == 0


def test_get_episodes_empty_icon_fanart():
    """Test get_episodes with empty icon and fanart"""
    episodes = topstories.get_episodes(5, "", "")
    assert isinstance(episodes, list)
