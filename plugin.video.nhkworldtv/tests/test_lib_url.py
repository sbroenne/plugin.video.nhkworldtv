from lib import nhk_api, url


# API request parameters
def test_get_API_request_params():
    assert url.get_api_request_params(nhk_api.rest_url["get_livestream"]) is not None


# JSON parsing
def test_get_JSON_invalid():
    """Test that get_json returns None for non-JSON content"""
    assert url.get_json("https://www3.nhk.or.jp/nhkworld/") is None


# URL construction
def test_get_NHK_website_url():
    """Test NHK website URL construction"""
    assert url.get_nhk_website_url("/nhkworld/") == "https://www3.nhk.or.jp/nhkworld/"
