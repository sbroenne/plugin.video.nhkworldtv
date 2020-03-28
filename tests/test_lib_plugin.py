import unittest  # The test framework
import lib.plugin as plugin

class Test_Navigation_Menus(unittest.TestCase):

    def test_main_menu_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_main_menu_add_live_stream_menu_item(self):
        self.assertTrue(plugin.add_live_stream_menu_item())

    def test_main_menu(self):
        self.assertTrue(plugin.index())

    def test_vod_menu_get_programs(self):
        detail_url = plugin.vod_programs()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_vod_menu__get_categories(self):
        detail_url = plugin.vod_categories()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_vod_menu_get_playlists(self):
        detail_url = plugin.vod_playlists()
        print(detail_url)
        self.assertIsNotNone(detail_url)

    def test_vod_menu(self):
        self.assertTrue(plugin.vod_index())
    
if __name__ == '__main__':
    unittest.main()
