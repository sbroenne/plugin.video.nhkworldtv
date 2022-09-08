from lib import ataglance, episode


def test_get_menu_item():
    # Test if a Episode is returned
    assert isinstance(ataglance.get_menu_item(), episode.Episode)


def test_get_episodes():
    episodes = ataglance.get_episodes(2000)
    # Test if a list is returned and that the list is not empty
    assert isinstance(episodes, list)
    assert len(episodes) > 0


def test_get_episodes_with_max_items10():
    max_items = 10
    episodes = ataglance.get_episodes(max_items)
    # Test if a list is returned and that the list is not empty
    assert len(episodes) == max_items
