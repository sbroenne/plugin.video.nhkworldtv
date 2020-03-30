import unittest  # The test framework
from lib.episode import Episode
from datetime import datetime


class Test_Test_Episode(unittest.TestCase):

    _now = datetime.now

    def test_create_episode(self):
        episode = Episode()
        self.assertIsNotNone(episode)

    def test_set_thumb_nhk(self):
        episode = Episode()
        episode.thumb = "/nhkworld/test.gif"
        print(episode.thumb)
        self.assertTrue('https://' in episode.thumb)

    def test_set_thumb_no_nhk(self):
        episode = Episode()
        test_url = 'https://test.gif'
        episode.thumb = test_url
        print(episode.thumb)
        self.assertEqual(test_url, episode.thumb)

    def test_get_video_info_from_string(self):
        episode = Episode()
        episode.video_info = '123'
        self.assertIsNotNone(episode.video_info)

    def test_get_video_info_from_values(self):
        episode = Episode()
        episode.aspect = 1
        episode.width = 2
        episode.height = 3
        vi = episode.video_info
        self.assertIsNotNone(vi)


if __name__ == '__main__':
    unittest.main()
