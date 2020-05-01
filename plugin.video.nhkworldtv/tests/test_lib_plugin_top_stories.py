import unittest  # The test framework
import lib.plugin as plugin


class Test_Top_Stories(unittest.TestCase):
    def test_add_top_stories_menu_item(self):
        self.assertTrue(plugin.add_top_stories_menu_item())

    def test_get_top_stories_index(self):
        self.assertIsNotNone(plugin.top_stories_index())


if __name__ == '__main__':
    unittest.main()
