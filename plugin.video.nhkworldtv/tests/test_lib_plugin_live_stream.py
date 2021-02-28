import lib.plugin as plugin
import lib.url as url
import lib.nhk_api as nhk_api

# Check the that the live stream URL can be accessed
# It changes from time to time!


def test_nhk_api_live_stream_url_720p():
    assert (url.get_url(nhk_api.rest_url['live_stream_url_720p'],
                        False).status_code == 200)


def test_nhk_api_live_stream_url_1080p():
    assert (url.get_url(nhk_api.rest_url['live_stream_url_1080p'],
                        False).status_code == 200)


# Kodi live stream menu items
def test_main_menu_add_on_demand_menu_item():
    assert (plugin.add_on_demand_menu_item() is True)


def test_main_menu_add_live_stream_menu_item_720p():
    episode = plugin.add_live_stream_menu_item(use_720p=True)
    assert (episode.url is not None)
    assert (episode.video_info["height"] == "720")


def test_main_menu_add_live_stream_menu_item_1080p():
    episode = plugin.add_live_stream_menu_item(use_720p=False)
    assert (episode.url is not None)
    assert (episode.video_info["height"] == "1080")
