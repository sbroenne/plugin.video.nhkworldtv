import xbmcplugin

from lib import plugin

# Episode lists


def test_get_programs_episodes():
    program_id = plugin.vod_programs()
    assert program_id is not None
    assert (
        plugin.vod_episode_list(
            "get_programs_episode_list",
            program_id,
            1,
            xbmcplugin.SORT_METHOD_TITLE,
            unit_test=True,
        )
        is True
    )


def test_get_categories_episodes():
    category_id = plugin.vod_categories()
    assert category_id is not None
    assert (
        plugin.vod_episode_list(
            "get_categories_episode_list",
            category_id,
            0,
            xbmcplugin.SORT_METHOD_TITLE,
            unit_test=True,
        )
        is True
    )


def test_get_latest_episodes():
    assert (
        plugin.vod_episode_list(
            "get_latest_episodes",
            "None",
            0,
            xbmcplugin.SORT_METHOD_DATE,
            unit_test=True,
        )
        is True
    )


def test_get_mostwatched_episodes():
    assert (
        plugin.vod_episode_list(
            "get_most_watched_episodes",
            "None",
            0,
            xbmcplugin.SORT_METHOD_NONE,
            unit_test=True,
        )
        is True
    )


def test_get_all_episodes_no_unit_test():
    assert (
        plugin.vod_episode_list(
            "get_all_episodes", "None", 0, xbmcplugin.SORT_METHOD_NONE, unit_test=False
        )
        is True
    )
