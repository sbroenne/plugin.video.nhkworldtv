import unittest   # The test framework
from lib.utils import get_url, get_json, get_NHK_website_url, to_local_time
from lib.nhk_api import rest_url
import requests
import datetime
from pytz import timezone
from tzlocal import get_localzone

class Test_Test_utils(unittest.TestCase):
    def test_get_HTTPS(self):
        self.assertIsInstance(get_url('https://www3.nhk.or.jp/nhkworld/', False), requests.Response)
    
    def test_get_api(self):
        self.assertIsInstance(get_url(rest_url['get_livestream'], True), requests.Response)

    def test_get_JSON(self):
        self.assertIsInstance(get_json(rest_url['get_livestream']), dict)

    def test_get_NHK_website_url(self):
        self.assertEqual(get_NHK_website_url('/nhkworld/'),'https://www3.nhk.or.jp/nhkworld/')

    def test_to_local_time(self):
        converted_time = to_local_time(1581266400000/1000)
        local_tz = get_localzone()
        local_time = local_tz.localize(datetime.datetime(year=2020, month=2, day=9, hour=17, minute=40))
        self.assertEqual(local_time, converted_time)

      
if __name__ == '__main__':
    unittest.main()
