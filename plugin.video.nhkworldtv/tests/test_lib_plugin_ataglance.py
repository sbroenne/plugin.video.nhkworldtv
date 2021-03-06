import unittest  # The test framework
import lib.plugin as plugin


class Test_AtAGlance(unittest.TestCase):
    def test_add_AtAGlance_menu_item(self):
        self.assertTrue(plugin.add_ataglance_menu_item())

    def test_get_AtAGlance_index(self):
        self.assertIsNotNone(plugin.ataglance_index())


if __name__ == '__main__':
    unittest.main()
