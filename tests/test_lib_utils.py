import datetime
import unittest  # The test framework

import requests
import tzlocal

import lib.nhk_api as nhk_api
import lib.utils as utils


class Test_Test_utils(unittest.TestCase):
    def test_get_HTTPS(self):
        self.assertIsInstance(
            utils.get_url('https://www3.nhk.or.jp/nhkworld/'),
            requests.Response)

    def test_get_JSON(self):
        self.assertIsInstance(
            utils.get_json(nhk_api.rest_url['get_livestream']), dict)

    def test_get_NHK_website_url(self):
        self.assertEqual(utils.get_NHK_website_url('/nhkworld/'),
                         'https://www3.nhk.or.jp/nhkworld/')

    def test_to_local_time(self):
        converted_time = utils.to_local_time(1581266400000 / 1000)
        local_tz = tzlocal.get_localzone()
        local_time = local_tz.localize(
            datetime.datetime(year=2020, month=2, day=9, hour=17, minute=40))
        self.assertEqual(local_time, converted_time)


if __name__ == '__main__':
    unittest.main()
