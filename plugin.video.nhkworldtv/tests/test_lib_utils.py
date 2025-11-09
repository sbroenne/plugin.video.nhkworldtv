"""
Utility functions
"""

import datetime

from lib import utils


def test_get_episode_name():
    title = "title"
    subtitle = "subtitle"
    assert utils.get_episode_name(title, subtitle) == title + " - " + subtitle
    assert utils.get_episode_name(title, "") == title


def test_to_local_time():
    converted_time = utils.to_local_time(1581266400000 // 1000)
    assert isinstance(converted_time, datetime.datetime)


def test_get_top_stories_play_path():
    xmltext = "rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/20200322_18_73446_HQ.mp4"
    assert utils.get_topstories_play_path(xmltext) == "20200322_18_73446_"


def test_get_ataglance_play_path():
    xmltext = "<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/aag_handmademask.mp4</file.high>"
    assert utils.get_ataglance_play_path(xmltext) == "aag_handmademask.mp4"


def test_get_local_timestamp_from_news_datestring():
    datestring = "20200416130000"
    local_datetime = utils.get_timestamp_from_datestring(datestring)
    assert local_datetime is not None


def test_format_plot():
    plot = utils.format_plot("Line 1", "Line 2")
    assert "Line 1" in plot
    assert "Line 2" in plot
    assert "\n\n" in plot


def test_to_local_time_overflow():
    """Test to_local_time with overflow timestamp"""
    # Very large timestamp that causes overflow
    large_timestamp = 99999999999999
    result = utils.to_local_time(large_timestamp)
    # Should return datetime.max instead of crashing
    from datetime import datetime

    assert result == datetime.max


def test_get_top_stories_play_path_no_match():
    """Test get_top_stories_play_path when no match found"""
    xml_text = "<xml><file>test.mp4</file></xml>"
    result = utils.get_topstories_play_path(xml_text)
    assert result is None


def test_get_top_stories_play_path_with_match():
    """Test get_top_stories_play_path with valid match"""
    xml_text = (
        "rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/test123HQ"
    )
    result = utils.get_topstories_play_path(xml_text)
    assert result == "test123"


def test_get_ataglance_play_path_no_match():
    """Test get_ataglance_play_path when no match found"""
    xml_text = "<xml><file>test.mp4</file></xml>"
    result = utils.get_ataglance_play_path(xml_text)
    assert result is None


def test_get_ataglance_play_path_with_match():
    """Test get_ataglance_play_path with valid match"""
    xml_text = "<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/test456</file.high>"
    result = utils.get_ataglance_play_path(xml_text)
    assert result == "test456"


def test_get_episode_name_empty_subtitle():
    """Test get_episode_name with empty subtitle"""
    name = utils.get_episode_name("Main Title", "")
    assert name == "Main Title"


def test_get_episode_name_with_subtitle():
    """Test get_episode_name with both title and subtitle"""
    name = utils.get_episode_name("Main Title", "Subtitle")
    assert name == "Main Title - Subtitle"
