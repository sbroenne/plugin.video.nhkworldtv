"""
Test episode functionality
"""

import pytest

from lib import plugin, vod
from lib.episode import Episode


@pytest.fixture
def test_episode():
    episodes = vod.get_episode_list("get_latest_episodes", "None", 0)

    assert isinstance(episodes, list)
    no_of_episodes = len(episodes)
    assert no_of_episodes > 0
    # Get the second oldest episode - ensures that this is in the Azure Cache
    episode = episodes[no_of_episodes - 1]
    assert isinstance(episode, Episode)
    return episode


# Directly playable episode


def test_add_playable_episode_cached_720p(test_episode):

    return_value = plugin.add_playable_episode(
        test_episode, use_720p=True, use_cache=True
    )
    assert isinstance(return_value, list)
    path = return_value[0]
    assert "http://" in path


def test_add_playable_episode_cached_1080p(test_episode):

    return_value = plugin.add_playable_episode(
        test_episode, use_720p=False, use_cache=True
    )
    assert isinstance(return_value, list)
    path = return_value[0]
    assert "http://" in path


# Episode that needs to be resolved from NHK
def test_add_playable_episode_needs_to_be_resolved(test_episode):

    return_value = plugin.add_playable_episode(
        test_episode, use_720p=False, use_cache=False
    )
    assert isinstance(return_value, list)
    path = return_value[0]
    assert "plugin:///" in path


# Resolve URLs from NHK
def test_get_media_information_api_url(test_episode):
    vod_id = test_episode.vod_id
    assert vod.get_media_information_api_url(vod_id).startswith('https://api01-platform.stream.co.jp/apiservice/getMediaByParam/')


def test_resolve_episode_from_NHK_720p(test_episode):

    resolved_episode = plugin.resolve_vod_episode(test_episode.vod_id, use_720p=True)
    assert resolved_episode.url is not None
    assert resolved_episode.video_info["height"] == "720"

