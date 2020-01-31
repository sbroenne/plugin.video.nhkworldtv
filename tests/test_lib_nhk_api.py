import unittest   # The test framework
from lib.nhk_api import rest_url

class Test_Test_nhk_api(unittest.TestCase):
    def test_nhk_api_episodes(self):
        self.assertIsNotNone(rest_url['get_all_episodes'])

    def test_nhk_api_live_stream_url(self):
        self.assertIsNotNone(rest_url['live_stream_url'])
    
    def test_nhk_api_player_url(self):
        self.assertIsNotNone(rest_url['player_url'])

    def test_nhk_api_video_url(self):
        self.assertIsNotNone(rest_url['video_url'])

    def test_nhk_api_episode_url(self):
        self.assertIsNotNone(rest_url['episode_url'])

if __name__ == '__main__':
    unittest.main()
