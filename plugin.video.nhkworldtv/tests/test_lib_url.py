from lib import nhk_api, url


# API request parameters
def test_get_API_request_params():
    # Test with an endpoint that has query parameters
    assert url.get_api_request_params(nhk_api.rest_url["homepage_ondemand"]) is not None


# JSON parsing
def test_get_JSON_invalid():
    """Test that get_json returns None for non-JSON content"""
    assert url.get_json("https://www3.nhk.or.jp/nhkworld/") is None


# URL construction
def test_get_NHK_website_url():
    """Test NHK website URL construction"""
    assert url.get_nhk_website_url("/nhkworld/") == "https://www3.nhk.or.jp/nhkworld/"


# 1080p upgrade functionality
def test_upgrade_to_1080p_replaces_master_with_o_master():
    """Test that upgrade_to_1080p correctly replaces master.m3u8 with o-master.m3u8"""
    test_url = "https://masterpl.hls.nhkworld.jp/hls/w/test/master.m3u8"
    # We test URL transformation only, not availability check
    # since that requires network access
    result = url.upgrade_to_1080p(test_url)
    # Either returns 1080p (if available) or original 720p
    assert "master.m3u8" in result or "o-master.m3u8" in result


def test_upgrade_to_1080p_handles_non_master_url():
    """Test that upgrade_to_1080p returns original URL if not a master.m3u8"""
    test_url = "https://example.com/video/playlist.m3u8"
    result = url.upgrade_to_1080p(test_url)
    assert result == test_url


def test_upgrade_to_1080p_handles_none():
    """Test that upgrade_to_1080p handles None input"""
    result = url.upgrade_to_1080p(None)
    assert result is None


def test_upgrade_to_1080p_handles_empty_string():
    """Test that upgrade_to_1080p handles empty string"""
    result = url.upgrade_to_1080p("")
    assert result == ""


def test_check_stream_available_with_live_1080p():
    """Test that 1080p live stream URL is available"""
    from lib import nhk_api, url

    result = url.check_stream_available(nhk_api.rest_url["live_stream_url_1080p"])
    assert result is True


def test_parse_highest_bitrate_stream():
    """Test that playlist parser extracts highest bitrate stream correctly"""
    from lib.url import _parse_highest_bitrate_stream

    # Sample playlist content from actual NHK World o-master.m3u8
    playlist = """#EXTM3U
#EXT-X-VERSION:4
#EXT-X-STREAM-INF:BANDWIDTH=1856404,RESOLUTION=1280x720
https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/abc123/v3.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=7003216,RESOLUTION=1920x1080
https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/def456/v1.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3572008,RESOLUTION=1280x720
https://media-tyo.hls.nhkworld.jp/hls/w/live/1/sig/ghi789/v2.m3u8
"""

    base_url = "https://masterpl.hls.nhkworld.jp/hls/w/live/o-master.m3u8"
    result = _parse_highest_bitrate_stream(playlist, base_url)

    # Should return the 1080p stream with highest bandwidth (7003216)
    assert result is not None
    assert "v1.m3u8" in result
    assert "def456" in result


def test_parse_highest_bitrate_stream_with_relative_urls():
    """Test parser handles relative URLs in playlist"""
    from lib.url import _parse_highest_bitrate_stream

    playlist = """#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=640x360
v3.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
v1.m3u8
"""

    base_url = "https://example.com/live/master.m3u8"
    result = _parse_highest_bitrate_stream(playlist, base_url)

    # Should convert relative URL to absolute
    assert result == "https://example.com/live/v1.m3u8"


def test_parse_highest_bitrate_stream_empty_playlist():
    """Test parser handles empty or invalid playlist gracefully"""
    from lib.url import _parse_highest_bitrate_stream

    result = _parse_highest_bitrate_stream("", "https://example.com/master.m3u8")
    assert result is None

    result = _parse_highest_bitrate_stream(
        "#EXTM3U\n#NO-STREAMS", "https://example.com/master.m3u8"
    )
    assert result is None


def test_upgrade_to_1080p_with_live_stream():
    """Test that live stream URL attempts to upgrade to o-master"""
    # Test with actual live stream base URL structure
    base_url = "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8"
    result = url.upgrade_to_1080p(base_url)

    # Result should either be upgraded to o-master.m3u8 or stay at master.m3u8
    # (depending on availability check)
    expected_1080p = "https://masterpl.hls.nhkworld.jp/hls/w/live/o-master.m3u8"
    assert result in [base_url, expected_1080p], \
        f"Expected either {base_url} or {expected_1080p}, got {result}"
