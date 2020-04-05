from __future__ import division
from past.utils import old_div
import datetime
import unittest  # The test framework
import requests

import lib.nhk_api as nhk_api
import lib.utils as utils


class Test_Test_utils(unittest.TestCase):
    def test_get_HTTPS(self):
        self.assertIsInstance(
            utils.get_url('https://www3.nhk.or.jp/nhkworld/'),
            requests.Response)

    def test_get_JSON_cached(self):
        self.assertIsInstance(
            utils.get_json(nhk_api.rest_url['get_livestream']), dict)

    def test_get_JSON_non_cached(self):
        self.assertIsInstance(
            utils.get_json(nhk_api.rest_url['get_livestream'], False), dict)

    def test_get_NHK_website_url(self):
        self.assertEqual(utils.get_NHK_website_url('/nhkworld/'),
                         'https://www3.nhk.or.jp/nhkworld/')

    def test_to_local_time(self):
        converted_time = utils.to_local_time(old_div(1581266400000, 1000))
        local_time = datetime.datetime(year=2020,
                                       month=2,
                                       day=9,
                                       hour=17,
                                       minute=40)
        self.assertEqual(local_time, converted_time)

    def test_get_top_stories_play_path(self):
        xmltext = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/20200322_18_73446_HQ.mp4'
        self.assertEqual(utils.get_top_stories_play_path(xmltext),
                         '20200322_18_73446_')

    def test_get_ataglance_play_path(self):
        xmltext = '<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/aag_handmademask.mp4</file.high>'
        self.assertEqual(utils.get_ataglance_play_path(xmltext),
                         'aag_handmademask.mp4')

    def test_get_metadata_cache(self):
        cache = utils.get_program_metdadata_cache(100)
        self.assertIsNotNone(cache)


if __name__ == '__main__':
    unittest.main()
