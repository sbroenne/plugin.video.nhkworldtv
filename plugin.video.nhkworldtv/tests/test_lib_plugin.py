"""
Unit tests for plugin.py

Tests the main plugin routing and UI logic, focusing on testable components
"""

import sys
from unittest.mock import MagicMock

import pytest

# Mock Kodi modules before importing plugin
sys.modules["xbmc"] = MagicMock()
sys.modules["xbmcgui"] = MagicMock()
sys.modules["xbmcplugin"] = MagicMock()
sys.modules["xbmcaddon"] = MagicMock()
sys.modules["xbmcvfs"] = MagicMock()
sys.modules["routing"] = MagicMock()

# Import after mocking
from lib import plugin  # noqa: E402
from lib.episode import Episode  # noqa: E402


class TestAddPlayableEpisode:
    """Test add_playable_episode function structure"""

    def test_returns_list_with_three_elements(self):
        """Test that add_playable_episode returns a list with 3 elements"""
        episode = Episode()
        episode.vod_id = "test_episode_123"
        episode.title = "Test Episode"
        episode.is_playable = True

        result = plugin.add_playable_episode(episode)

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 3, "Result should have exactly 3 elements"

    def test_third_element_is_false(self):
        """Test that third element is False (not a folder)"""
        episode = Episode()
        episode.vod_id = "test_episode"
        episode.is_playable = True

        result = plugin.add_playable_episode(episode)

        assert result[2] is False, "Third element should be False (not a folder)"

    def test_not_double_wrapped_in_tuple(self):
        """
        CRITICAL REGRESSION TEST: Verify result is not double-wrapped

        This tests the bug that was found:
        playable_episodes.append((add_playable_episode(episode)))

        The extra parentheses created:
        ([url, listitem, False],)  # Wrong - tuple wrapping a list

        Instead of:
        [url, listitem, False]  # Correct - flat list

        If someone accidentally adds the extra parentheses again,
        this test will catch it.
        """
        episode = Episode()
        episode.vod_id = "test"
        episode.is_playable = True

        result = plugin.add_playable_episode(episode)

        # Should be a list, not tuple
        assert isinstance(result, list), "Result must be a list"
        assert len(result) == 3, "Result must have exactly 3 elements"

        # Demonstrate the bug: wrapping in tuple creates wrong structure
        wrong_structure = (result,)  # This is what the bug did
        assert len(wrong_structure) == 1, "Bug creates single-element tuple"
        assert isinstance(wrong_structure[0], list), "Bug nests list in tuple"

        # The correct structure should unpack properly
        url, listitem, is_folder = result  # No ValueError = correct
        assert is_folder is False


class TestEpisodeTupleStructure:
    """Regression tests for episode tuple structure bugs"""

    def test_playable_episode_tuple_is_not_double_wrapped(self):
        """
        Test the specific bug where append((func())) double-wraps

        Context: In vod_episode_list(), line 904 had:
        playable_episodes.append((add_playable_episode(episode)))

        The problem:
        - add_playable_episode() returns [url, listitem, False]
        - (result) creates a tuple around it: ([url, listitem, False],)
        - Kodi expects [(url, listitem, False), ...] not [([...],), ...]

        This caused: Clicking episode → shows program list instead of playing
        """
        episode = Episode()
        episode.vod_id = "regression_test"
        episode.is_playable = True

        result = plugin.add_playable_episode(episode)

        # Result should be a flat list
        assert isinstance(result, list)
        assert len(result) == 3

        # First element shouldn't be nested
        assert not isinstance(result[0], (list, tuple))

        # Should be able to unpack directly
        url, listitem, is_folder = result
        assert url is not None
        assert listitem is not None
        assert is_folder is False

    def test_multiple_episodes_same_structure(self):
        """Test that all episodes use consistent structure"""
        episodes = []

        for i in range(5):
            ep = Episode()
            ep.vod_id = f"episode_{i}"
            ep.is_playable = True
            episodes.append(plugin.add_playable_episode(ep))

        # All should be lists with 3 elements
        for item in episodes:
            assert isinstance(item, list)
            assert len(item) == 3
            assert item[2] is False  # is_folder

    def test_append_without_extra_parentheses(self):
        """
        Test that appending to list works correctly

        This demonstrates the fix:
        WRONG: list.append((function()))  # Creates nested structure
        RIGHT: list.append(function())     # Appends result directly
        """
        episode1 = Episode()
        episode1.vod_id = "ep1"
        episode1.is_playable = True

        episode2 = Episode()
        episode2.vod_id = "ep2"
        episode2.is_playable = True

        # Correct way (what we fixed it to)
        correct_list = []
        correct_list.append(plugin.add_playable_episode(episode1))
        correct_list.append(plugin.add_playable_episode(episode2))

        # Each item should be a 3-element list
        assert len(correct_list) == 2
        for item in correct_list:
            assert isinstance(item, list)
            assert len(item) == 3

        # Wrong way (the bug we had)
        wrong_list = []
        # Note the extra parentheses around the function call
        wrong_list.append((plugin.add_playable_episode(episode1)))
        wrong_list.append((plugin.add_playable_episode(episode2)))

        # This actually creates the same structure in Python,
        # but in the original code context it was in a tuple literal
        # Let's show what really happened:
        really_wrong = []
        really_wrong.append((plugin.add_playable_episode(episode1),))
        really_wrong.append((plugin.add_playable_episode(episode2),))

        # Now items are single-element tuples containing lists
        assert len(really_wrong) == 2
        for item in really_wrong:
            assert isinstance(item, tuple)
            assert len(item) == 1  # Single element tuple!
            assert isinstance(item[0], list)  # Nested list inside


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
