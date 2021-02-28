from __future__ import division
import lib.nhk_api as nhk_api
import lib.url as url


# Valid URLs
def test_check_url_exists():
    assert (url.check_url_exists('https://www3.nhk.or.jp/nhkworld/') is True)


def test_get_API_request_params():
    assert (url.get_API_request_params(nhk_api.rest_url['get_livestream'])
            is not None)


def test_request_url():
    assert (url.request_url('https://www3.nhk.or.jp/nhkworld/',
                            False).status_code == 200)


def test_get_url():
    assert (url.get_url('https://www3.nhk.or.jp/nhkworld/',
                        False).status_code == 200)


# Non-existing URLs
def test_request_url_notexists():
    assert (url.request_url('http://doesnotexist', False).status_code == 10001)


def test_get_url_notexists():
    assert (url.get_url('http://doesnotexist', False).status_code == 10001)


# Not found URLs


def test_request_url_notfound():
    assert (url.get_url('https://www3.nhk.or.jp/doesnotexist/',
                        False).status_code == 404)


# JSON


def test_get_JSON_cached():
    assert (isinstance(url.get_json(nhk_api.rest_url['get_livestream']), dict))


def test_get_JSON_non_cached():
    assert (isinstance(url.get_json(nhk_api.rest_url['get_livestream'], False),
                       dict))


def test_get_JSON_invalid():
    assert (url.get_json('https://www3.nhk.or.jp/nhkworld/') is None)


def test_get_JSON_notexists():
    assert (url.get_json('http://doesnotexist') is None)


def test_get_NHK_website_url():
    assert (url.get_NHK_website_url('/nhkworld/') ==
            'https://www3.nhk.or.jp/nhkworld/')
