from __future__ import (unicode_literals)
import lib.plugin as plugin
import lib.url as url
import lib.ataglance as ataglance
import lib.topstories as topstories


def test_play_news_item_from_top_stories():
    topstories_episodes = topstories.get_episodes(1, "", "")
    assert (topstories_episodes is not None)
    episode = topstories_episodes[0]
    api_url_string = '/nhkworld/data/en/news/movie/{0}.xml'.format(
        episode.vod_id)
    api_url = url.get_NHK_website_url(api_url_string)
    assert (plugin.play_news_item(api_url, episode.vod_id, 'news',
                                  episode.title) is True)


def test_play_news_item_from_ataglance():
    ataglance_episodes = ataglance.get_episodes(1)
    assert (ataglance_episodes is not None)
    episode = ataglance_episodes[0]
    assert (episode is not None)
    api_url_string = '/nhkworld/en/news/ataglance/{0}/video-main.xml'.format(
        episode.vod_id)
    api_url = url.get_NHK_website_url(api_url_string)
    assert (plugin.play_news_item(api_url, episode.vod_id, 'ataglance',
                                  episode.title) is True)


def test_play_news_item_invalid_option():
    assert (plugin.play_news_item('Unit Test', 'Unit Test', 'invalid option',
                                  'Unit Test') is False)
