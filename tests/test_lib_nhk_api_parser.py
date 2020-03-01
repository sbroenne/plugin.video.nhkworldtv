import unittest  # The test framework
import lib.nhk_api_parser as parser


class Test_NHK_api_parser(unittest.TestCase):
    def test_get_API_from_NHK(self):
        self.assertIsNotNone(parser.get_API_from_NHK())

    def test_replace_path_parameters_version_language(self):
        path = 'vodrecommend/{version}/{lang}/list.json'
        self.assertEqual('vodrecommend/v7a/en/list.json',
                         parser.replace_path_parameters_version_language(path, 'v7a', 'en'))

    def test_get_homepage_ondemand_url(self):
        self.assertEqual('https://api.nhk.or.jp/nhkworld/vodrecommend/v7a/en/list.json', parser.get_homepage_ondemand_url())

    def test_get_homepage_news_url(self):
        self.assertEqual('https://www3.nhk.or.jp/nhkworld/data/en/news/all.json', parser.get_homepage_news_url())

    def test_get_livestream_url(self):
        self.assertEqual('https://api.nhk.or.jp/nhkworld/epg/v7a/world/now.json', parser.get_livestream_url())

if __name__ == '__main__':
    unittest.main()
