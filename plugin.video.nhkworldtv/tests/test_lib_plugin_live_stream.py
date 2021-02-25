import unittest  # The test framework
import lib.plugin as plugin
import lib.utils as utils
import lib.nhk_api as nhk_api


class Test_Live_Stream(unittest.TestCase):

    # Check the that the live stream URL can be accessed
    # It changes from time to time!

    def test_nhk_api_live_stream_url_720p(self):
        self.assertTrue(
            utils.get_url(nhk_api.rest_url['live_stream_url_720p'],
                          False).status_code == 200)

    def test_nhk_api_live_stream_url_1080p(self):
        self.assertTrue(
            utils.get_url(nhk_api.rest_url['live_stream_url_1080p'],
                          False).status_code == 200)

    # Kodi live stream menu items
    def test_main_menu_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_main_menu_add_live_stream_menu_item_720p(self):
        episode = plugin.add_live_stream_menu_item(use_720p=True)
        print(episode.url)
        self.assertIsNotNone(episode.url)
        self.assertEqual(episode.video_info["height"], "720")

    def test_main_menu_add_live_stream_menu_item_1080p(self):
        episode = plugin.add_live_stream_menu_item(use_720p=False)
        print(episode.url)
        self.assertIsNotNone(episode.url)
        self.assertEqual(episode.video_info["height"], "1080")


if __name__ == '__main__':
    unittest.main()
