from lib import episode, topstories


def test_get_menu_item():
    # Test if a Episode is returned
    assert isinstance(topstories.get_menu_item(), episode.Episode)


def test_get_episodes():
    episodes = topstories.get_episodes(2000, "icon", "fanart")
    # Test if a list is returned and that the list is not empty
    assert isinstance(episodes, list)
    assert len(episodes) > 0


def test_get_episodes_with_max_items10():
    max_items = 10
    episodes = topstories.get_episodes(max_items, "", "")
    # Test if a list is returned and that the list is not empty
    assert isinstance(episodes, list)
    assert len(episodes) == max_items
