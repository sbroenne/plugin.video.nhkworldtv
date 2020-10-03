from __future__ import print_function
import unittest  # The test framework
import lib.plugin as plugin
import xbmcplugin


class Test_VOD(unittest.TestCase):
    def test_get_programs_episodes(self):
        program_id = plugin.vod_programs()
        self.assertIsNotNone(program_id)
        episode = plugin.vod_episode_list('get_programs_episode_list',
                                          program_id, 1,
                                          xbmcplugin.SORT_METHOD_TITLE)
        self.assertIsNotNone(episode)

    def test_get_categories_episodes(self):
        category_id = plugin.vod_categories()
        self.assertIsNotNone(category_id)
        episode = plugin.vod_episode_list('get_categories_episode_list',
                                          category_id, 0,
                                          xbmcplugin.SORT_METHOD_TITLE)
        self.assertIsNotNone(episode)

    def test_get_playlists_episodes(self):
        playlist_id = plugin.vod_playlists()
        self.assertIsNotNone(playlist_id)
        episode = plugin.vod_episode_list('get_playlists_episode_list',
                                          playlist_id, 0,
                                          xbmcplugin.SORT_METHOD_TITLE)
        self.assertIsNotNone(episode)

    def test_get_latest_episodes(self):
        episode = plugin.vod_episode_list('get_latest_episodes', 'None', 0,
                                          xbmcplugin.SORT_METHOD_DATE)
        self.assertIsNotNone(episode)

    def test_get_mostwatched_episodes_cached(self):
        episode = plugin.vod_episode_list('get_most_watched_episodes', 'None',
                                          0, xbmcplugin.SORT_METHOD_NONE, True)
        self.assertIsNotNone(episode)

    def test_get_mostwatched_episodes_non_cached(self):
        episode = plugin.vod_episode_list('get_most_watched_episodes', 'None',
                                          0, xbmcplugin.SORT_METHOD_NONE)
        self.assertIsNotNone(episode)

    def test_play_episode_non_cache(self):

        episode = plugin.vod_episode_list('get_most_watched_episodes', 'None',
                                          0, xbmcplugin.SORT_METHOD_NONE)
        self.assertIsNotNone(episode)
        episode_url = plugin.play_vod_episode(episode.vod_id, True)
        print(episode_url)
        self.assertIsNotNone(episode_url)
  
    def test_play_episode_cache(self):

        episode = plugin.vod_episode_list('get_most_watched_episodes', 'None',
                                          0, xbmcplugin.SORT_METHOD_NONE, '')
        self.assertIsNotNone(episode)
        episode_url = plugin.play_vod_episode(episode.vod_id, False)
        print(episode_url)
        self.assertIsNotNone(episode_url)


if __name__ == '__main__':
    unittest.main()
