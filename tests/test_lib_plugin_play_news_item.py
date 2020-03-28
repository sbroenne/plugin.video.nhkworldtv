import unittest  # The test framework
import lib.plugin as plugin
import lib.utils as utils

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

if __name__ == '__main__':
    unittest.main()
