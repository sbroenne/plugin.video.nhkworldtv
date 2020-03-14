import unittest  # The test framework

import xbmcplugin

import lib.nhk_api as nhk_api
import lib.plugin as plugin


class Test_Navigation_Menus(unittest.TestCase):
    def test_main_menu(self):
        self.assertTrue(plugin.index())

    def test_vod_menu(self):
        self.assertTrue(plugin.vod_index())


class Test_Main_Menu_Items(unittest.TestCase):
    def test_add_top_stories_menu_item(self):
        self.assertTrue(plugin.add_top_stories_menu_item())

    def test_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_add_live_stream_menu_item(self):
        self.assertTrue(plugin.add_live_stream_menu_item())

    def test_add_live_schedule_menu_item(self):
        self.assertTrue(plugin.add_live_schedule_menu_item())


class Test_VOD_Menus(unittest.TestCase):
    def test_get_programs(self):
        detail_url = plugin.vod_programs()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_get_categories(self):
        detail_url = plugin.vod_categories()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_get_playlists(self):
        detail_url = plugin.vod_playlists()
        print(detail_url)
        self.assertIsNotNone(detail_url)


class Test_VOD_Episode_List(unittest.TestCase):
    def test_get_programs_episodes(self):
        test_url = plugin.vod_programs()
        vid_id = plugin.vod_episode_list(test_url, 1, 0,
                                         xbmcplugin.SORT_METHOD_TITLE)
        # print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_categories_episodes(self):
        test_url = plugin.vod_categories()
        vid_id = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_TITLE)
        # print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_playlists_episodes(self):
        test_url = plugin.vod_playlists()
        vid_id = plugin.vod_episode_list(test_url, 0, 1,
                                         xbmcplugin.SORT_METHOD_TITLE)
        # print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_latest_episodes(self):
        test_url = nhk_api.rest_url['get_latest_episodes']
        vid_id = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_DATEADDED)
        # print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_mostwatched_episodes(self):
        test_url = nhk_api.rest_url['get_most_watched_episodes']
        vid_id = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE, True)
        print(vid_id)
        self.assertIsNotNone(vid_id)


class Test_Top_Stories(unittest.TestCase):
    def test_get_top_stories_list(self):
        row_count = plugin.top_stories_list()
        print(row_count)
        self.assertIsNot(row_count, 0)


class Test_Live_Schedule(unittest.TestCase):
    def test_get_live_schedule_index(self):
        self.assertTrue(plugin.live_schedule_index())


class Test_VOD_Episode_Play_NonCache(unittest.TestCase):
    def test_show_episode(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        vid_id = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
        print(vid_id)

        episode_url = plugin.show_episode(vid_id, '2019',
                                          '2020-01-01 12:00:00', False)
        print(episode_url)
        self.assertIsNotNone(episode_url)

class Test_VOD_Episode_Play_Cache(unittest.TestCase):
    def test_show_episode(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        vid_id = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
        print(vid_id)

        episode_url = plugin.show_episode(vid_id, '2019',
                                          '2020-01-01 12:00:00', True)
        print(episode_url)
        self.assertIsNotNone(episode_url)

    def test_get_episode_cache(self):
        self.assertIsNotNone(plugin.get_episode_cache())

if __name__ == '__main__':
    unittest.main()
