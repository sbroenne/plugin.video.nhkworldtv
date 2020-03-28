import unittest  # The test framework
import lib.plugin as plugin
import lib.nhk_api as nhk_api
import xbmcplugin

class Test_VOD(unittest.TestCase):
    def test_get_programs_episodes(self):
        test_url = plugin.vod_programs()
        episode = plugin.vod_episode_list(test_url, 1,
                                         xbmcplugin.SORT_METHOD_LABEL)
        self.assertGreater(len(episode.title),0)

    def test_get_categories_episodes(self):
        test_url = plugin.vod_categories()
        episode = plugin.vod_episode_list(test_url, 0,
                                         xbmcplugin.SORT_METHOD_LABEL)
        self.assertGreater(len(episode.title),0)

    def test_get_playlists_episodes(self):
        test_url = plugin.vod_playlists()
        episode = plugin.vod_episode_list(test_url, 0,
                                         xbmcplugin.SORT_METHOD_LABEL)
        self.assertGreater(len(episode.title),0)


    def test_get_latest_episodes(self):
        test_url = nhk_api.rest_url['get_latest_episodes']
        episode = plugin.vod_episode_list(test_url, 0,
                                         xbmcplugin.SORT_METHOD_DATE)
        self.assertGreater(len(episode.title),0)


    def test_get_mostwatched_episodes_cached(self):
        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0,
                                         xbmcplugin.SORT_METHOD_NONE, True)
        self.assertGreater(len(episode.title),0)


    def test_get_mostwatched_episodes_non_cached(self):
        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
        self.assertGreater(len(episode.title),0)

    def test_play_episode_non_cache(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
        episode_url = plugin.play_vod_episode(episode.vod_id, False)
        print(episode_url)
        self.assertIsNotNone(episode_url)

    def test_play_episode_cache(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
      
        episode_url = plugin.play_vod_episode(episode.vod_id, True)
        print(episode_url)
        self.assertIsNotNone(episode_url)

if __name__ == '__main__':
    unittest.main()
