import unittest   # The test framework
import lib.nhk_api as nhk_api


class Test_Test_nhk_api(unittest.TestCase):
    def test_nhk_api_episodes(self):
        self.assertIsNotNone(nhk_api.rest_url['get_all_episodes'])

    def test_nhk_api_live_stream_url(self):
        self.assertIsNotNone(nhk_api.rest_url['live_stream_url'])

    def test_nhk_api_player_url(self):
        self.assertIsNotNone(nhk_api.rest_url['player_url'])

    def test_nhk_api_video_url(self):
        self.assertIsNotNone(nhk_api.rest_url['video_url'])

    def test_nhk_api_episode_url(self):
        self.assertIsNotNone(nhk_api.rest_url['episode_url'])


if __name__ == '__main__':
    unittest.main()
