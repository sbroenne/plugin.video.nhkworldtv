import unittest  # The test framework

import xbmcplugin

import lib.nhk_api as nhk_api
import lib.plugin as plugin
import lib.utils as utils
from lib.episode import Episode


class Test_Navigation_Menus(unittest.TestCase):
    def test_main_menu(self):
        self.assertTrue(plugin.index())

    def test_vod_menu(self):
        self.assertTrue(plugin.vod_index())


class Test_Main_Menu_Items(unittest.TestCase):

    def test_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_add_live_stream_menu_item(self):
        self.assertTrue(plugin.add_live_stream_menu_item())



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


class Test_Top_Stories(unittest.TestCase):
    def test_add_top_stories_menu_item(self):
        self.assertTrue(plugin.add_top_stories_menu_item())
    
    def test_get_top_stories_index(self):
        self.assertIsNot(plugin.top_stories_index(), 0)

class Test_AtAGlance(unittest.TestCase):
    def test_add_AtAGlance_menu_item(self):
        self.assertTrue(plugin.add_ataglance_menu_item())
    
    def test_get_AtAGlance_index(self):
        self.assertIsNot(plugin.ataglance_index(), 0)

class Test_Play_News_Item(unittest.TestCase):
    def test_play_news_item_from_top_stories(self):
        api_url_string = u'/nhkworld/data/en/news/movie/20200322_18.xml'
        api_url = utils.get_NHK_website_url(api_url_string)
        news_id = 822
        title = u'Global coronavirus deaths exceed 10,000'
        self.assertTrue(plugin.play_news_item(api_url, news_id, 'news', title))

    def test_play_news_item_from_ataglance(self):
        api_url_string = u'/nhkworld/en/news/ataglance/822/video-main.xml'
        api_url = utils.get_NHK_website_url(api_url_string)
        news_id = u'20200322_18'
        title = u'Teen makes masks for elderly, orphans'
        self.assertTrue(plugin.play_news_item(api_url, news_id, 'ataglance', title))
    
    def test_play_news_item_invalid(self):
        api_url_string = u'/nhkworld/en/news/ataglance/822/video-main.xml'
        api_url = utils.get_NHK_website_url(api_url_string)
        news_id = u'20200322_18'
        title = u'Teen makes masks for elderly, orphans'
        self.assertFalse(plugin.play_news_item(api_url, news_id, 'invalid', title))


class Test_Live_Schedule(unittest.TestCase):
    def test_add_live_schedule_menu_item(self):
        self.assertTrue(plugin.add_live_schedule_menu_item())

    def test_get_live_schedule_index(self):
        self.assertIsNot(plugin.live_schedule_index(True), 0)


class Test_VOD_Episode_Play_Cache(unittest.TestCase):
    def test_show_episode_non_cache(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
        episode_url = plugin.show_episode(episode.vod_id, False)
        print(episode_url)
        self.assertIsNotNone(episode_url)

    def test_show_episode_cache(self):

        test_url = nhk_api.rest_url['get_most_watched_episodes']
        episode = plugin.vod_episode_list(test_url, 0, 0,
                                         xbmcplugin.SORT_METHOD_NONE)
      
        episode_url = plugin.show_episode(episode.vod_id, True)
        print(episode_url)
        self.assertIsNotNone(episode_url)

    def test_get_episode_cache(self):
        self.assertIsNotNone(plugin.get_program_metdadata_cache())

if __name__ == '__main__':
    unittest.main()
