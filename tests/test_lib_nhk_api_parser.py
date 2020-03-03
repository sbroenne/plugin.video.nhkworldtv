import unittest  # The test framework
import lib.nhk_api_parser as parser


class Test_NHK_api_parser(unittest.TestCase):
    def test_get_API_from_NHK(self):
        self.assertIsNotNone(parser.get_API_from_NHK())

    def test_replace_path_parameters_version_language(self):
        path = 'vodrecommend/{version}/{lang}/list.json'
        self.assertEqual(u'vodrecommend/v7a/en/list.json',
                         parser.replace_path_parameters_version_language(path, 'v7a', 'en'))

    def test_get_homepage_ondemand_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodrecommend/v7a/en/list.json', parser.get_homepage_ondemand_url())

    def test_get_homepage_news_url(self):
        self.assertEqual(u'https://www3.nhk.or.jp/nhkworld/data/en/news/all.json', parser.get_homepage_news_url())

    def test_get_livestream_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/epg/v7a/world/now.json', parser.get_livestream_url())

    def test_get_programs_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodpglist/v7a/en/voice/list.json', parser.get_programs_url())

    def test_get_programs_episode_list_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/program/{0}/en/all/all.json', parser.get_programs_episode_list_url())
    
    def test_get_categories_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodcatlist/v7a/all/en/ondemand/list.json', parser.get_categories_url())
   
    def test_get_categories_episode_list_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/category/{0}/en/all/all.json', parser.get_categories_episode_list_url())
   
    def test_get_playlists_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodplaylist/v7a/en/all.json', parser.get_playlists_url())

    def test_get_playlists_episode_list_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodplaylist/v7a/en/{0}.json', parser.get_playlists_episode_list_url())

    def test_get_latest_episodes_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/all/all/en/all/12.json', parser.get_all_episodes_url('12'))
                           
    def test_get_most_watched_episodes_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/mostwatch/all/en/all/all.json', parser.get_most_watched_episodes_url())
  
    def test_get_all_episodes_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/all/all/en/all/all.json', parser.get_all_episodes_url('all'))
  
    def test_get_episode_detail_url(self):
        self.assertEqual(u'https://api.nhk.or.jp/nhkworld/vodesdlist/v7a/vod_id/{0}/en/all/1.json', parser.get_episode_detail_url())
  
if __name__ == '__main__':
    unittest.main()
