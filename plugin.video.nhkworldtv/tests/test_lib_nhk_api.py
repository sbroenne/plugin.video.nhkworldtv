from lib import nhk_api


# Test hardcoded API URL constants exist
def test_nhk_api_endpoints_defined():
    """Verify that essential API endpoints are defined as constants"""
    assert "homepage_ondemand" in nhk_api.rest_url
    assert "get_livestream" in nhk_api.rest_url
    assert "get_latest_episodes" in nhk_api.rest_url
    assert nhk_api.rest_url["homepage_ondemand"] is not None
    assert nhk_api.rest_url["get_livestream"] is not None
    assert nhk_api.rest_url["get_latest_episodes"] is not None
