""" 
Test API Parser
"""

import lib.nhk_api_parser as parser


def test_get_API_from_NHK():
    assert parser.get_api_from_nhk() is not None


def test_replace_path_parameters_version_language():
    path = "vodrecommend/{version}/{lang}/list.json"
    assert (
        "vodrecommend/v7b/en/list.json"
        == parser.replace_path_parameters_version_language(path, "v7b", "en")
    )


def test_get_homepage_ondemand_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/mostwatch/all/en/all/all.json"
        == parser.get_homepage_ondemand_url()
    )


def test_get_homepage_news_url():
    assert (
        "https://www3.nhk.or.jp/nhkworld/data/en/news/all.json"
        == parser.get_homepage_news_url()
    )


def test_get_livestream_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/epg/v7b/world/now.json"
        == parser.get_livestream_url()
    )


def test_get_programs_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodpglist/v7b/en/voice/list.json"
        == parser.get_programs_url()
    )


def test_get_programs_episode_list_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/program/{0}/en/all/all.json"
        == parser.get_programs_episode_list_url()
    )


def test_get_categories_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodcatlist/v7b/all/en/ondemand/list.json"
        == parser.get_categories_url()
    )


def test_get_categories_episode_list_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/category/{0}/en/all/all.json"
        == parser.get_categories_episode_list_url()
    )



def test_get_latest_episodes_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/all/all/en/all/12.json"
        == parser.get_all_episodes_url("12")
    )


def test_get_most_watched_episodes_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/mostwatch/all/en/all/all.json"
        == parser.get_most_watched_episodes_url()
    )


def test_get_all_episodes_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/all/all/en/all/all.json"
        == parser.get_all_episodes_url("all")
    )


def test_get_episode_detail_url():
    assert (
        "https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/vod_id/{0}/en/all/1.json"
        == parser.get_episode_detail_url()
    )
