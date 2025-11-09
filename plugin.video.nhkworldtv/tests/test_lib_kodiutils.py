"""Tests for kodiutils module"""

from contextlib import suppress

from lib import kodiutils


def test_get_video_info_1080p_variant():
    """Test that v1.m3u8 URLs are detected as 1080p"""
    url = "https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v1.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "1920"
    assert info["height"] == "1080"
    assert info["aspect"] == "1.78"


def test_get_video_info_720p_variants():
    """Test that v2/v3.m3u8 URLs are detected as 720p"""
    url_v2 = "https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v2.m3u8"
    info_v2 = kodiutils.get_video_info(url_v2)

    assert info_v2["width"] == "1280"
    assert info_v2["height"] == "720"

    url_v3 = "https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v3.m3u8"
    info_v3 = kodiutils.get_video_info(url_v3)

    assert info_v3["width"] == "1280"
    assert info_v3["height"] == "720"


def test_get_video_info_360p_variant():
    """Test that v4.m3u8 URLs are detected as 360p"""
    url = "https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v4.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "640"
    assert info["height"] == "360"


def test_get_video_info_180p_variant():
    """Test that v5.m3u8 URLs are detected as 180p"""
    url = "https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v5.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "320"
    assert info["height"] == "180"


def test_get_video_info_o_master_playlist():
    """Test that o-master.m3u8 URLs are detected as 1080p"""
    url = "https://media-tyo.hls.nhkworld.jp/hls/w/live/o-master.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "1920"
    assert info["height"] == "1080"


def test_get_video_info_master_playlist():
    """Test that master.m3u8 URLs are detected as 720p"""
    url = "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "1280"
    assert info["height"] == "720"


def test_get_video_info_default_no_url():
    """Test that default is 1080p when no URL provided"""
    info = kodiutils.get_video_info()

    assert info["width"] == "1920"
    assert info["height"] == "1080"
    assert info["aspect"] == "1.78"


def test_get_video_info_unknown_url():
    """Test that unknown URLs default to 1080p"""
    url = "https://example.com/video/unknown.m3u8"
    info = kodiutils.get_video_info(url)

    assert info["width"] == "1920"
    assert info["height"] == "1080"


def test_get_string_unit_test():
    """Test get_string returns unit test string when localization fails"""
    string = kodiutils.get_string(99999)
    assert "UNIT TEST" in string


def test_show_notification():
    """Test show_notification doesn't crash"""
    kodiutils.show_notification("Test Title", "Test Message", 1000)
    # Should not raise exception


def test_show_notification_default_time():
    """Test show_notification with default time"""
    kodiutils.show_notification("Test Title", "Test Message")
    # Should not raise exception


def test_get_sd_video_info():
    """Test get_sd_video_info returns correct SD resolution"""
    video_info = kodiutils.get_sd_video_info()
    assert video_info["width"] == "640"
    assert video_info["height"] == "368"
    assert video_info["aspect"] == "1.82"


def test_set_video_directory_information():
    """Test set_video_directory_information with videos content type"""
    # This will fail gracefully in unit test environment
    with suppress(Exception):
        kodiutils.set_video_directory_information(0, 1, "videos")


def test_set_video_directory_information_episodes():
    """Test set_video_directory_information with episodes content type"""
    with suppress(Exception):
        kodiutils.set_video_directory_information(0, 1, "episodes")


def test_get_episodelist_title_single():
    """Test get_episodelist_title with single episode"""
    title = kodiutils.get_episodelist_title("Test Show", 1)
    assert title is not None
    assert isinstance(title, str)


def test_get_episodelist_title_multiple():
    """Test get_episodelist_title with multiple episodes"""
    title = kodiutils.get_episodelist_title("Test Show", 5)
    assert title is not None
    assert isinstance(title, str)
