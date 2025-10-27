from lib import nhk_api, plugin, url
from lib.episode import Episode

# Check that the live stream URL can be accessed


def test_nhk_api_live_stream_url():
    assert (
        url.get_url(nhk_api.rest_url["live_stream_url"], False).status_code == 200
    )


# Kodi live stream menu items
def test_main_menu_add_on_demand_menu_item():
    episode = plugin.add_on_demand_menu_item()
    assert isinstance(episode, Episode)
    assert episode.title is not None


def test_main_menu_add_live_stream_menu_item():
    episode = plugin.add_live_stream_menu_item()
    assert isinstance(episode, Episode)
    assert episode.url is not None
    assert episode.video_info["height"] == "720"
