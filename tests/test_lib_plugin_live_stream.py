import unittest  # The test framework
import lib.plugin as plugin


class Test_Live_Stream(unittest.TestCase):
    def test_main_menu_add_on_demand_menu_item(self):
        self.assertTrue(plugin.add_on_demand_menu_item())

    def test_main_menu_add_live_stream_menu_item(self):
        self.assertTrue(plugin.add_live_stream_menu_item())


if __name__ == '__main__':
    unittest.main()
