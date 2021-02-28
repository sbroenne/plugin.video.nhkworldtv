import lib.news_programs as news_programs


def test_get_episodes():
    episodes = news_programs.get_programs()
    # Test if a list is returned and that the list is not empty
    assert (isinstance(episodes, list))
    assert (len(episodes) > 0)
