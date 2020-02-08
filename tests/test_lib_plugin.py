import unittest   # The test framework
from lib.plugin import index, add_live_stream, show_episode, vod_categories, vod_episode_list, vod_index, vod_playlists, vod_programs,rest_url
from xbmcplugin import SORT_METHOD_TITLE, SORT_METHOD_DATEADDED, SORT_METHOD_NONE

class Test_Test_Navigation_Menus(unittest.TestCase):
    def test_main_menu(self):
        self.assertTrue(index())
    
    def test_vod_menu(self):
        self.assertTrue(vod_index())

class Test_Test_Livestream(unittest.TestCase):

    def test_add_live_stream(self):
        
        self.assertTrue(add_live_stream())

class Test_Test_VOD_Menus(unittest.TestCase):

    def test_get_programs(self):
        detail_url = vod_programs()
        print(detail_url)
        self.assertIsNotNone(detail_url)
    
    def test_get_categories(self):
        detail_url = vod_categories()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_get_playlists(self):
        detail_url = vod_playlists()
        print(detail_url)
        self.assertIsNotNone(detail_url)


class Test_Test_VOD_Episode_List(unittest.TestCase):

    def test_get_programs_episodes(self):
        test_url=vod_programs()
        vid_id = vod_episode_list(test_url, 1, 0, SORT_METHOD_TITLE)
        #print(vid_id)
        self.assertIsNotNone(vid_id)
    
    def test_get_categories_episodes(self):
        test_url= vod_categories()
        vid_id = vod_episode_list(test_url, 0, 0, SORT_METHOD_TITLE)
        #print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_playlists_episodes(self):
        test_url= vod_playlists()
        vid_id = vod_episode_list(test_url, 0, 1, SORT_METHOD_TITLE)
        #print(vid_id)
        self.assertIsNotNone(vid_id)
    
    def test_get_latest_episodes(self):
        test_url=rest_url['get_latest_episodes']
        vid_id = vod_episode_list(test_url, 0, 0, SORT_METHOD_DATEADDED)
        #print(vid_id)
        self.assertIsNotNone(vid_id)

    
    def test_get_mostwatched_episodes(self):
        test_url=rest_url['get_most_watched_episodes']
        vid_id = vod_episode_list(test_url, 0, 0, SORT_METHOD_NONE)
        print(vid_id)
        self.assertIsNotNone(vid_id)

class Test_Test_VOD_Episode_Play(unittest.TestCase):

    def test_show_episode(self):

        test_url=rest_url['get_most_watched_episodes']
        vid_id = vod_episode_list(test_url, 0, 0, SORT_METHOD_NONE)
        
        episode_url = show_episode(  
                                        vid_id,
                                        '2019',
                                        '2020-01-01 12:00:00'
                                     )
        print(episode_url)
        self.assertIsNotNone(episode_url)

if __name__ == '__main__':
    unittest.main()
