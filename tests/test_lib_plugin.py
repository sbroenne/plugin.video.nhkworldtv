import unittest   # The test framework
from resources.lib.plugin import index, add_live_stream, show_episode, vod_categories, vod_episode_list, vod_index, vod_playlists, vod_programs

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
        #print(detail_url)
        self.assertIsNotNone(detail_url)
    
    def test_get_categories(self):
        detail_url = vod_categories()
        #print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_get_playlists(self):
        detail_url = vod_playlists()
        #print(detail_url)
        self.assertIsNotNone(detail_url)


class Test_Test_VOD_Episode_List(unittest.TestCase):

    def test_get_programs_episodelist(self):
        test_url='https://api.nhk.or.jp/nhkworld/vodesdlist/v7/program/closeup/en/all/all.json'
        vid_id = vod_episode_list(test_url, 1, 0)
        #print(vid_id)
        self.assertIsNotNone(vid_id)
    
    def test_get_categories_episodes(self):
        test_url='https://api.nhk.or.jp/nhkworld/vodesdlist/v7/category/18/en/all/all.json'
        vid_id = vod_episode_list(test_url, 0, 0)
        #print(vid_id)
        self.assertIsNotNone(vid_id)

    def test_get_playlists_episodes(self):
        test_url='https://api.nhk.or.jp/nhkworld/vodplaylist/v7/en/8.json'
        vid_id = vod_episode_list(test_url, 0, 1)
        #print(vid_id)
        self.assertIsNotNone(vid_id)

class Test_Test_VOD_Episode_Play(unittest.TestCase):

    def test_show_episode(self):
        
        episode_url = show_episode(  'UnitTest Episode', 
                                        'nw_vod_v_en_4002_764_20200118003000_01_1579277219',
                                        "UnitTest Plot",
                                        '180',
                                        '1',
                                        '2019',
                                        '2020-01-01 12:00:00'
                                     )
        #print(episode_url)
        self.assertIsNotNone(episode_url)

if __name__ == '__main__':
    unittest.main()
