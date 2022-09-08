"""
Test the news programs library
"""
import requests
from lib import news_programs


def test_get_news_programs_episodes():
    """Test news programs get episodes"""
    episodes = news_programs.get_programs()
    # Test if a list is returned and that the list is not empty
    assert isinstance(episodes, list)
    assert len(episodes) > 0
    # Issue #87 - Test that the episode play path returns a valid Url
    for episode in episodes:
        result = requests.get(episode[0], timeout=5)
        assert result.status_code, 200
