from __future__ import print_function
import lib.plugin as plugin
import xbmcplugin

# Episode lists


def test_get_programs_episodes():
    program_id = plugin.vod_programs()
    assert (program_id is not None)
    episode = plugin.vod_episode_list('get_programs_episode_list',
                                      program_id,
                                      1,
                                      xbmcplugin.SORT_METHOD_TITLE,
                                      unit_test=True)
    assert (episode is not None)


def test_get_categories_episodes():
    category_id = plugin.vod_categories()
    assert (category_id is not None)
    episode = plugin.vod_episode_list('get_categories_episode_list',
                                      category_id,
                                      0,
                                      xbmcplugin.SORT_METHOD_TITLE,
                                      unit_test=True)
    assert (episode is not None)


def test_get_playlists_episodes():
    playlist_id = plugin.vod_playlists()
    assert (playlist_id is not None)
    episode = plugin.vod_episode_list('get_playlists_episode_list',
                                      playlist_id,
                                      0,
                                      xbmcplugin.SORT_METHOD_TITLE,
                                      unit_test=True)
    assert (episode is not None)


def test_get_latest_episodes():
    episode = plugin.vod_episode_list('get_latest_episodes',
                                      'None',
                                      0,
                                      xbmcplugin.SORT_METHOD_DATE,
                                      unit_test=True)
    assert (episode is not None)


def test_get_mostwatched_episodes():
    episode = plugin.vod_episode_list('get_most_watched_episodes',
                                      'None',
                                      0,
                                      xbmcplugin.SORT_METHOD_NONE,
                                      unit_test=True)
    assert (episode is not None)
