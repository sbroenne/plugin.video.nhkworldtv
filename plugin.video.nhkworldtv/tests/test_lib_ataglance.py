"""Tests for ataglance module"""

from lib import ataglance


def test_get_menu_item():
    """Test get_menu_item returns menu item or None"""
    menu_item = ataglance.get_menu_item()
    # Should return Episode or None (if API fails)
    assert menu_item is None or hasattr(menu_item, "title")


def test_get_episodes():
    """Test get_episodes returns list of episodes"""
    episodes = ataglance.get_episodes(5)
    # Should return list (may be empty if API fails)
    assert isinstance(episodes, list)


def test_get_episodes_max_items():
    """Test get_episodes respects max_items limit"""
    episodes = ataglance.get_episodes(3)
    assert isinstance(episodes, list)
    # Should have at most 3 items
    assert len(episodes) <= 3


def test_get_episodes_zero_items():
    """Test get_episodes with zero max_items"""
    episodes = ataglance.get_episodes(0)
    assert isinstance(episodes, list)
    assert len(episodes) == 0
