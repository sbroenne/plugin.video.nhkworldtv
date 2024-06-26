import pytest
from lib import vod
from lib.episode import Episode


@pytest.fixture
def test_episode():
    return get_episode_from_episode_list()


def get_episode_from_episode_list():
    episodes = vod.get_episode_list("get_latest_episodes", "None", 0)
    no_of_episodes = len(episodes)
    # Get the second oldest episode - ensures that this is in the Azure Cache
    episode = episodes[no_of_episodes - 1]
    return episode



def test_get_episode_from_episode_list():
    episodes = vod.get_episode_list("get_latest_episodes", "None", 0)

    assert isinstance(episodes, list)
    no_of_episodes = len(episodes)
    assert no_of_episodes > 0
    # Get the second oldest episode - ensures that this is in the Azure Cache
    episode = episodes[no_of_episodes - 1]
    assert isinstance(episode, Episode)


def test_get_episode_from_cache_720p(test_episode):
    return_value = vod.get_episode_from_cache(test_episode, use_720p=True)
    path = return_value[0]
    assert "http://" in path


def test_get_episode_not_in_cache():
    episode = Episode()
    episode.vod_id = "not_in_cache"
    assert vod.get_episode_from_cache(episode) is None


def test_resolve_episode_720p(test_episode):
    assert isinstance(
        vod.resolve_vod_episode(test_episode.vod_id, use_720p=True), Episode
    )
    assert test_episode.is_playable is True
