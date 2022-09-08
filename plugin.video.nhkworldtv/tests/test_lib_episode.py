import time
from datetime import datetime, timedelta

from lib.episode import Episode


def test_create_episode():
    episode = Episode()
    assert episode.plot_include_time_difference is False


def test_set_thumb_nhk():
    episode = Episode()
    episode.thumb = "/nhkworld/test.gif"
    print((episode.thumb))
    assert "https://" in episode.thumb


def test_set_thumb_no_nhk():
    episode = Episode()
    test_url = "https://test.gif"
    episode.thumb = test_url
    print((episode.thumb))
    assert test_url == episode.thumb


def test_get_video_info_from_string():
    episode = Episode()
    episode.video_info = "123"
    assert episode.video_info is not None


def test_get_video_info_from_values():
    episode = Episode()
    episode.aspect = 1
    episode.width = 2
    episode.height = 3
    vi = episode.video_info
    assert vi is not None


def test_get_time_difference():
    episode = Episode()
    start_date = datetime.now() - timedelta(hours=1)
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp
    compare_date = datetime.now()
    time_difference = episode.get_time_difference(compare_date)
    assert time_difference is not None
    time_difference = episode.get_time_difference()
    assert time_difference is not None


def test_get_calculated_duration():
    episode = Episode()
    # Set the start date
    start_date = datetime.now()
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp

    # Set the end date (60 seconds later)
    end_date = start_date + timedelta(seconds=60)
    timestamp = time.mktime(end_date.timetuple()) * 1000
    episode.broadcast_end_date = timestamp
    assert episode.duration == 60


def test_get_plot_duration_time_difference():
    episode = Episode()
    # Set the start date
    start_date = datetime.now()
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp

    # Set the end date (60 seconds later)
    end_date = start_date + timedelta(seconds=90)
    timestamp = time.mktime(end_date.timetuple()) * 1000
    episode.broadcast_end_date = timestamp
    episode.plot_include_duration = True
    episode.plot_include_time_difference = True
    episode.plot = "Unit Test Plot"
    assert episode.kodi_list_item is not None
