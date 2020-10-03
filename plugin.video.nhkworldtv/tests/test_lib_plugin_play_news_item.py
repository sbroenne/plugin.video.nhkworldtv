from __future__ import (unicode_literals)
import unittest  # The test framework
import lib.plugin as plugin
import lib.utils as utils


class Test_Play_News_Item(unittest.TestCase):
    def test_play_news_item_from_top_stories(self):
        episode = plugin.top_stories_index()
        self.assertIsNotNone(episode)
        api_url_string = '/nhkworld/data/en/news/movie/{0}.xml'.format(
            episode.vod_id)
        api_url = utils.get_NHK_website_url(api_url_string)
        self.assertTrue(
            plugin.play_news_item(api_url, episode.vod_id, 'news',
                                  episode.title))

    def test_play_news_item_from_ataglance(self):
        episode = plugin.ataglance_index()
        self.assertIsNotNone(episode)
        api_url_string = '/nhkworld/en/news/ataglance/{0}/video-main.xml'.format(
            episode.vod_id)
        api_url = utils.get_NHK_website_url(api_url_string)
        self.assertTrue(
            plugin.play_news_item(api_url, episode.vod_id, 'ataglance',
                                  episode.title))

    def test_play_news_item_invalid_option(self):
        self.assertFalse(
            plugin.play_news_item('Unit Test', 'Unit Test', 'invalid option', 'Unit Test'))


if __name__ == '__main__':
    unittest.main()
