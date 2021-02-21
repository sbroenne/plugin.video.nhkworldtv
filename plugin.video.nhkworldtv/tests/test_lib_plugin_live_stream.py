import unittest  # The test framework
import lib.plugin as plugin
import lib.utils as utils
import lib.nhk_api as nhk_api


class Test_Live_Stream(unittest.TestCase):
    def test_main_menu_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_main_menu_add_live_stream_menu_item(self):
        self.assertTrue(plugin.add_live_stream_menu_item())

    # Check the that the live stream URL can be accessed - it changes from time to time!
    def test_nhk_api_live_stream_url(self):
        self.assertTrue(
            utils.get_url(nhk_api.rest_url['live_stream_url'],
                          False).status_code == 200)


if __name__ == '__main__':
    unittest.main()
