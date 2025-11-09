import time
from datetime import datetime, timedelta

from lib.episode import Episode


def test_create_episode():
    episode = Episode()
    assert episode.plot_include_time_difference is False


def test_set_thumb_nhk():
    episode = Episode()
    episode.thumb = "/nhkworld/test.gif"
    print(episode.thumb)
    assert "https://" in episode.thumb


def test_set_thumb_no_nhk():
    episode = Episode()
    test_url = "https://test.gif"
    episode.thumb = test_url
    print(episode.thumb)
    assert test_url == episode.thumb


def test_get_video_info_from_string():
    episode = Episode()
    episode.video_info = "123"
    assert episode.video_info is not None


def test_get_video_info_from_values():
    episode = Episode()
    episode.video_info = {"aspect": "1.78", "width": "1920", "height": "1080"}
    vi = episode.video_info
    assert vi is not None
    assert vi["width"] == "1920"


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
    episode.plot_include_time_difference = True
    episode.plot = "Unit Test Plot"
    assert episode.kodi_list_item is not None


def test_parse_timestamp_string_isdigit():
    """Test _parse_timestamp with string containing digits"""
    episode = Episode()
    timestamp_str = str(int(time.time() * 1000))
    episode.broadcast_start_date = timestamp_str
    assert episode.broadcast_start_date is not None


def test_parse_timestamp_iso_format():
    """Test _parse_timestamp with ISO 8601 format"""
    episode = Episode()
    iso_timestamp = "2025-10-28T20:00:00+09:00"
    episode.broadcast_start_date = iso_timestamp
    assert episode.broadcast_start_date is not None


def test_parse_timestamp_none():
    """Test _parse_timestamp with None value"""
    episode = Episode()
    episode.broadcast_start_date = None
    assert episode.broadcast_start_date is None


def test_normalize_url_empty():
    """Test _normalize_url with empty string"""
    episode = Episode()
    episode.thumb = ""
    assert episode.thumb == ""


def test_normalize_url_http():
    """Test _normalize_url with http URL"""
    episode = Episode()
    url = "http://example.com/image.jpg"
    episode.thumb = url
    assert episode.thumb == url


def test_normalize_url_https():
    """Test _normalize_url with https URL"""
    episode = Episode()
    url = "https://example.com/image.jpg"
    episode.thumb = url
    assert episode.thumb == url


def test_normalize_url_partial_with_absolute_flag():
    """Test _normalize_url with partial URL and absolute_image_url=True"""
    episode = Episode()
    episode.absolute_image_url = True
    url = "/nhkworld/test.jpg"
    episode.thumb = url
    assert episode.thumb == url


def test_normalize_url_partial_no_nhkworld():
    """Test _normalize_url with partial URL without /nhkworld/"""
    episode = Episode()
    url = "/other/path.jpg"
    episode.thumb = url
    assert episode.thumb == url


def test_fanart_normalization():
    """Test fanart property with URL normalization"""
    episode = Episode()
    episode.fanart = "/nhkworld/fanart.jpg"
    assert "https://" in episode.fanart


def test_fanart_none():
    """Test fanart property returns normalized URL"""
    episode = Episode()
    episode.fanart = "https://example.com/fanart.jpg"
    assert episode.fanart == "https://example.com/fanart.jpg"


def test_duration_none():
    """Test duration property returns None when not set"""
    episode = Episode()
    assert episode.duration is None


def test_date_property_none():
    """Test date property returns None when _date is None"""
    episode = Episode()
    assert episode.date is None


def test_aired_property_none():
    """Test aired property returns None when _aired is None"""
    episode = Episode()
    assert episode.aired is None


def test_year_property_none():
    """Test year property returns None when _date is None"""
    episode = Episode()
    assert episode.year is None


def test_video_info_property():
    """Test video_info property getter"""
    episode = Episode()
    assert episode.video_info is None
    episode.video_info = {"width": "1920"}
    assert episode.video_info["width"] == "1920"


def test_kodi_list_item_no_url():
    """Test kodi_list_item creation without URL"""
    episode = Episode()
    episode.title = "Test Episode"
    episode.plot = "Test plot"
    episode.thumb = "https://example.com/thumb.jpg"
    episode.fanart = "https://example.com/fanart.jpg"
    list_item = episode.kodi_list_item
    assert list_item is not None


def test_kodi_list_item_playable():
    """Test kodi_list_item with playable episode"""
    episode = Episode()
    episode.title = "Playable Episode"
    episode.plot = "Test plot"
    episode.url = "https://example.com/video.m3u8"
    episode.is_playable = True
    episode.thumb = "https://example.com/thumb.jpg"
    episode.video_info = {"width": "1920", "height": "1080"}
    list_item = episode.kodi_list_item
    assert list_item is not None


def test_get_info_label_basic():
    """Test get_info_label with basic episode data"""
    episode = Episode()
    episode.title = "Test Title"
    episode.plot = "Test Plot"
    info_label = episode.get_info_label()
    assert info_label["Title"] == "Test Title"
    assert info_label["Plot"] == "Test Plot"


def test_get_info_label_with_duration():
    """Test get_info_label includes duration"""
    episode = Episode()
    episode.title = "Test"
    episode.plot = "Test"
    episode.duration = 3600
    info_label = episode.get_info_label()
    assert info_label["Duration"] == 3600


def test_get_info_label_with_broadcast_detail():
    """Test get_info_label with broadcast detail"""
    episode = Episode()
    episode.title = "Test"
    episode.plot = "Test Plot"
    episode.plot_include_broadcast_detail = True
    end_date = datetime.now() + timedelta(days=7)
    timestamp = time.mktime(end_date.timetuple()) * 1000
    episode.broadcast_end_date = timestamp
    info_label = episode.get_info_label()
    assert "Plot" in info_label


def test_get_info_label_broadcast_detail_no_end_date():
    """Test get_info_label with broadcast_detail but no end_date"""
    episode = Episode()
    episode.title = "Test"
    episode.plot = "Test Plot"
    episode.plot_include_broadcast_detail = True
    info_label = episode.get_info_label()
    assert info_label["Plot"] == "Test Plot"


def test_get_info_label_with_all_fields():
    """Test get_info_label with all possible fields"""
    episode = Episode()
    episode.title = "Complete Episode"
    episode.plot = "Complete Plot"
    episode.duration = 1800
    episode.pgm_no = 42
    episode.playcount = 3

    start_date = datetime.now()
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp

    info_label = episode.get_info_label()
    assert info_label["Title"] == "Complete Episode"
    assert info_label["Duration"] == 1800
    assert info_label["Episode"] == 42
    assert info_label["playcount"] == 3
    assert "Year" in info_label
    assert "date" in info_label
    assert "aired" in info_label


def test_get_time_difference_days():
    """Test get_time_difference with days difference"""
    episode = Episode()
    start_date = datetime.now() - timedelta(days=2)
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp
    time_diff = episode.get_time_difference()
    assert "," in time_diff  # Should contain formatted date


def test_get_time_difference_minutes():
    """Test get_time_difference with minutes"""
    episode = Episode()
    start_date = datetime.now() - timedelta(minutes=30)
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp
    time_diff = episode.get_time_difference()
    assert time_diff is not None


def test_get_time_difference_one_hour():
    """Test get_time_difference with exactly 1 hour"""
    episode = Episode()
    start_date = datetime.now() - timedelta(hours=1, seconds=30)
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp
    time_diff = episode.get_time_difference()
    assert time_diff is not None


def test_get_time_difference_multiple_hours():
    """Test get_time_difference with multiple hours"""
    episode = Episode()
    start_date = datetime.now() - timedelta(hours=5)
    timestamp = time.mktime(start_date.timetuple()) * 1000
    episode.broadcast_start_date = timestamp
    time_diff = episode.get_time_difference()
    assert time_diff is not None
