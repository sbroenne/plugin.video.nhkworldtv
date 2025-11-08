"""Tests for kodiutils module"""

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
