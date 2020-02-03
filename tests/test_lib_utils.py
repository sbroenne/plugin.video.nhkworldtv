import unittest   # The test framework
from lib.utils import get_url, get_json, get_NHK_website_url
from lib.nhk_api import rest_url
import requests

class Test_Test_utils(unittest.TestCase):
    def test_get_HTTPS(self):
        self.assertIsInstance(get_url('https://www3.nhk.or.jp/nhkworld/', False), requests.Response)
    
    def test_get_api(self):
        self.assertIsInstance(get_url(rest_url['get_livestream'], True), requests.Response)

    def test_get_JSON(self):
        self.assertIsInstance(get_json(rest_url['get_livestream']), dict)

    def test_get_NHK_wesbite_url(self):
        self.assertEqual(get_NHK_website_url('/nhkworld/'),'https://www3.nhk.or.jp/nhkworld/')

      
if __name__ == '__main__':
    unittest.main()
