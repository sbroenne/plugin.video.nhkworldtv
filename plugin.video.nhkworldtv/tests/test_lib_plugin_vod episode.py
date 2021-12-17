from __future__ import print_function
import lib.plugin as plugin
import lib.vod as vod
import pytest


@pytest.fixture
def test_episode():
    episodes = vod.get_episode_list('get_latest_episodes', 'None', 0)
    assert (isinstance(episodes, list))
    assert (len(episodes) > 0)
    episode = episodes[1]
    return episode


# Directly playable episode


def test_add_playable_episode_cached_720p(test_episode):

    return_value = plugin.add_playable_episode(test_episode,
                                               use_720p=True,
                                               use_cache=True)
    assert (isinstance(return_value, list))
    path = return_value[0]
    assert ("https://" in path)


def test_add_playable_episode_cached_1080p(test_episode):

    return_value = plugin.add_playable_episode(test_episode,
                                               use_720p=False,
                                               use_cache=True)
    assert (isinstance(return_value, list))
    path = return_value[0]
    assert ("https://" in path)


# Episode that needs to be resolved from NHK
def test_add_playable_episode_needs_to_be_resolved(test_episode):

    return_value = plugin.add_playable_episode(test_episode,
                                               use_720p=False,
                                               use_cache=False)
    assert (isinstance(return_value, list))
    path = return_value[0]
    assert ("plugin:///" in path)


# Resolve URLs from NHK


def test_resolve_episode_from_NHK_720p(test_episode):

    resolved_episode = plugin.resolve_vod_episode(test_episode.vod_id,
                                                  use_720p=True)
    assert (resolved_episode.url is not None)
    assert (resolved_episode.video_info["height"] == "720")


def test_resolve_episode_from_NHK_1080p(test_episode):
    resolved_episode = plugin.resolve_vod_episode(test_episode.vod_id,
                                                  use_720p=False)
    assert (resolved_episode.url is not None)
    assert (resolved_episode.video_info["height"] == "1080")
