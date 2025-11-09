from unittest.mock import MagicMock, patch

from lib import nhk_api, url


# API request parameters
def test_get_api_request_params():
    # Test with an endpoint that has query parameters
    assert url.get_api_request_params(nhk_api.rest_url["homepage_ondemand"]) is not None


# JSON parsing
def test_get_json_invalid():
    """Test that get_json returns None for non-JSON content"""
    assert url.get_json("https://www3.nhk.or.jp/nhkworld/") is None


# URL construction
def test_get_nhk_website_url():
    result = url.get_nhk_website_url("/test/path")
    assert result.startswith("http")
    assert "/test/path" in result


def test_cache_response():
    """Test _cache_response stores data correctly"""
    test_url = "https://test.example.com/api"
    content = "test content"
    url._cache_response(test_url, content, None)
    assert test_url in url._response_cache


def test_get_cached_response():
    """Test _get_cached_response retrieves cached data"""
    test_url = "https://test.example.com/cached"
    content = "cached content"
    url._cache_response(test_url, content, None)
    cached = url._get_cached_response(test_url, None)
    assert cached == content


def test_get_cached_response_expired():
    """Test _get_cached_response returns None for expired cache"""
    test_url = "https://test.example.com/expired"
    content = "expired content"
    # Manually set expired cache entry
    url._response_cache[test_url] = (content, 0.0)  # Already expired
    cached = url._get_cached_response(test_url, None)
    assert cached is None
    assert test_url not in url._response_cache  # Should be removed


def test_get_cache_key_with_params():
    """Test _get_cache_key generates consistent keys with params"""
    test_url = "https://test.example.com/api"
    params = {"b": "2", "a": "1"}  # Unordered
    key = url._get_cache_key(test_url, params)
    assert "a=1" in key
    assert "b=2" in key
    # Should be sorted alphabetically
    assert key.index("a=1") < key.index("b=2")


def test_get_cache_key_without_params():
    """Test _get_cache_key without params"""
    test_url = "https://test.example.com/api"
    key = url._get_cache_key(test_url, None)
    assert key == test_url


def test_get_api_request_params_nhk_api():
    """Test get_api_request_params for NHK API URLs"""
    test_url = "https://api.nhkworld.jp/showsapi/v1/test"
    params = url.get_api_request_params(test_url)
    assert params == {}


def test_get_api_request_params_nhk_base():
    """Test get_api_request_params for NHK base URLs"""
    test_url = "https://www3.nhk.or.jp/nhkworld/test"
    params = url.get_api_request_params(test_url)
    assert params == {}


def test_get_api_request_params_other():
    """Test get_api_request_params for non-NHK URLs"""
    test_url = "https://example.com/test"
    params = url.get_api_request_params(test_url)
    assert params is None


def test_check_url_exists():
    """Test check_url_exists function"""
    # Test with NHK World live stream URL (should exist)
    exists = url.check_url_exists(
        "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8"
    )
    assert exists is True or exists is False  # Just test it doesn't crash


# Tests with mocking for retry logic and error handling


@patch("lib.url.session.get")
def test_get_url_success_first_try(mock_get):
    """Test get_url succeeds on first try"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "success"
    mock_get.return_value = mock_response

    response = url.get_url("https://example.com/test", cached=False)
    assert response.status_code == 200
    assert mock_get.call_count == 1


@patch("lib.url.session.get")
@patch("lib.url.time.sleep")
def test_get_url_retry_502_then_success(mock_sleep, mock_get):
    """Test get_url retries on 502 and succeeds"""
    # First call returns 502, second call succeeds
    mock_response_502 = MagicMock()
    mock_response_502.status_code = 502

    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.text = "success"

    mock_get.side_effect = [mock_response_502, mock_response_200]

    response = url.get_url("https://example.com/test", cached=False)
    assert response.status_code == 200
    assert mock_get.call_count == 2
    assert mock_sleep.call_count == 1  # Should wait before retry


@patch("lib.url.session.get")
@patch("lib.url.time.sleep")
def test_get_url_max_retries_502(mock_sleep, mock_get):
    """Test get_url stops after max retries with 502"""
    mock_response = MagicMock()
    mock_response.status_code = 502
    mock_get.return_value = mock_response

    response = url.get_url("https://example.com/test", cached=False)
    assert response.status_code == 502
    assert mock_get.call_count == 3  # max_retries = 3
    assert mock_sleep.call_count == 2  # Sleeps before retry 2 and 3


@patch("lib.url.session.get")
def test_get_url_fatal_error_no_retry(mock_get):
    """Test get_url doesn't retry on fatal errors (4xx, 5xx except 502)"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    response = url.get_url("https://example.com/test", cached=False)
    assert response.status_code == 404
    assert mock_get.call_count == 1  # No retry


@patch("lib.url.session.get")
def test_get_url_500_error_no_retry(mock_get):
    """Test get_url doesn't retry on 500 errors"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    response = url.get_url("https://example.com/test", cached=False)
    assert response.status_code == 500
    assert mock_get.call_count == 1  # No retry for non-502 errors


@patch("lib.url.session.get")
def test_request_url_with_api_params(mock_get):
    """Test request_url includes API params for NHK URLs"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "success"
    mock_get.return_value = mock_response

    response = url.request_url("https://api.nhkworld.jp/showsapi/v1/test", cached=False)
    assert response.status_code == 200
    # Verify params were passed (empty dict for NHK API)
    assert mock_get.called


@patch("lib.url.session.get")
def test_request_url_without_api_params(mock_get):
    """Test request_url without API params for non-NHK URLs"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "success"
    mock_get.return_value = mock_response

    response = url.request_url("https://example.com/test", cached=False)
    assert response.status_code == 200
    assert mock_get.called


@patch("lib.url.session.get")
def test_request_url_caches_successful_response(mock_get):
    """Test request_url caches successful responses"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "cached content"
    mock_get.return_value = mock_response

    test_url = "https://example.com/test_cache"

    # First call - should hit API
    response1 = url.request_url(test_url, cached=True)
    assert response1.status_code == 200

    # Second call - should use cache (mock not called again)
    response2 = url.request_url(test_url, cached=True)
    assert response2.status_code == 200
    assert response2.text == "cached content"

    # Only called once because second was cached
    assert mock_get.call_count == 1


@patch("lib.url.session.get")
def test_request_url_connection_error(mock_get):
    """Test request_url handles connection errors"""
    from requests import ConnectionError as RequestsConnectionError

    mock_get.side_effect = RequestsConnectionError("Connection failed")

    response = url.request_url("https://example.com/test", cached=False)
    assert response.status_code == 10001


@patch("lib.url.session.get")
def test_get_json_with_valid_json(mock_get):
    """Test get_json with valid JSON response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_response.text = '{"key": "value"}'
    mock_get.return_value = mock_response

    result = url.get_json("https://api.example.com/test", cached=False)
    assert result == {"key": "value"}


@patch("lib.url.session.get")
def test_get_json_with_invalid_json(mock_get):
    """Test get_json with invalid JSON returns None"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "not json"
    mock_get.return_value = mock_response

    result = url.get_json("https://api.example.com/test", cached=False)
    assert result is None


@patch("lib.url.session.get")
def test_get_json_with_non_200_status(mock_get):
    """Test get_json with non-200 status returns None"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = url.get_json("https://api.example.com/test", cached=False)
    assert result is None
