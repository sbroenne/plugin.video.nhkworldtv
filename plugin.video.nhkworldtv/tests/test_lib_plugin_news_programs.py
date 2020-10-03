import unittest  # The test framework
import lib.plugin as plugin


class Test_News_Programs(unittest.TestCase):
    def test_get_news_programs_index(self):
        self.assertIsNotNone(plugin.news_programs_index())


if __name__ == '__main__':
    unittest.main()
