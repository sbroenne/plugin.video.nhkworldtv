from __future__ import print_function
import unittest  # The test framework
from lib.episode import Episode
from datetime import datetime, timedelta
import time


class Test_Test_Episode(unittest.TestCase):
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

    def test_set_bandwidth(self):
        episode = Episode()
        mbit = 0.5
        episode.title = 'Test'
        episode.bandwidth = mbit * 1000 * 1000
        listItem = episode.kodi_list_item
        self.assertIsNotNone(listItem.getProperty('network.bandwidth'))

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

    def test_get_time_difference(self):
        episode = Episode()
        start_date = datetime.now() - timedelta(hours=1)
        timestamp = time.mktime(start_date.timetuple()) * 1000
        episode.broadcast_start_date = timestamp
        compare_date = datetime.now()
        time_difference = episode.get_time_difference(compare_date)
        self.assertIsNotNone(time_difference)
        time_difference = episode.get_time_difference()
        self.assertIsNotNone(time_difference)

    def test_get_calculated_duration(self):
        episode = Episode()
        # Set the start date
        start_date = datetime.now()
        timestamp = time.mktime(start_date.timetuple()) * 1000
        episode.broadcast_start_date = timestamp

        # Set the end date (60 seeconds later)
        end_date = start_date + timedelta(seconds=60)
        timestamp = time.mktime(end_date.timetuple()) * 1000
        episode.broadcast_end_date = timestamp
        self.assertIs(episode.duration, 60)

    def test_get_plot_duration_time_difference(self):
        episode = Episode()
        # Set the start date
        start_date = datetime.now()
        timestamp = time.mktime(start_date.timetuple()) * 1000
        episode.broadcast_start_date = timestamp

        # Set the end date (60 seeconds later)
        end_date = start_date + timedelta(seconds=90)
        timestamp = time.mktime(end_date.timetuple()) * 1000
        episode.broadcast_end_date = timestamp
        episode.plot_include_duration = True
        episode.plot_include_time_difference = True
        episode.plot = 'Unit Test Plot'
        self.assertIsNotNone(episode.kodi_list_item)


if __name__ == '__main__':
    unittest.main()
