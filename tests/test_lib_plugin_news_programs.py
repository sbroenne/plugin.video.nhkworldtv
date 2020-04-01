import unittest  # The test framework
import lib.plugin as plugin


class Test_News_Programs(unittest.TestCase):
    def test_get_news_programs_index(self):
        self.assertIsNot(plugin.news_programs_index(), 0)


if __name__ == '__main__':
    unittest.main()
