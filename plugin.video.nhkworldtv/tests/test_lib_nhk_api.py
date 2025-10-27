from lib import nhk_api, url


# Test hardcoded API URL endpoint
def test_nhk_api_ondemand_url():
    assert url.get_url(nhk_api.rest_url["homepage_ondemand"], False).status_code == 200
