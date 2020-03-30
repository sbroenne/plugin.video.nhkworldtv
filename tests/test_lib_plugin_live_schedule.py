import unittest  # The test framework
import lib.plugin as plugin


class Test_Live_Schedule(unittest.TestCase):
    def test_add_live_schedule_menu_item(self):
        self.assertTrue(plugin.add_live_schedule_menu_item())

    def test_get_live_schedule_index(self):
        self.assertIsNot(plugin.live_schedule_index(), 0)


if __name__ == '__main__':
    unittest.main()
