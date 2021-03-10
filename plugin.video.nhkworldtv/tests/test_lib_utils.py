from __future__ import division
import datetime

import lib.utils as utils


def test_get_episode_name():
    title = "title"
    subtitle = "subtitle"
    assert (utils.get_episode_name(title,
                                   subtitle) == title + " - " + subtitle)
    assert (utils.get_episode_name(title, "") == title)


def test_to_local_time():
    converted_time = utils.to_local_time(1581266400000 // 1000)
    assert (isinstance(converted_time, datetime.datetime))


def test_get_top_stories_play_path():
    xmltext = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/20200322_18_73446_HQ.mp4'
    assert (utils.get_top_stories_play_path(xmltext) == '20200322_18_73446_')


def test_get_ataglance_play_path():
    xmltext = '<file.high>rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/english/news/ataglance/aag_handmademask.mp4</file.high>'
    assert (utils.get_ataglance_play_path(xmltext) == 'aag_handmademask.mp4')


def test_get_news_program_play_path():
    xmltext = 'rtmp://flv.nhk.or.jp/ondemand/flv/nhkworld/upld/medias/en/news/programs/1001_20200413171930_hq.mp4'
    assert (
        utils.get_news_program_play_path(xmltext) == '1001_20200413171930_')


def test_get_local_timestamp_from_news_datestring():
    datestring = '20200416130000'
    local_datetime = utils.get_timestamp_from_datestring(datestring)
    assert (local_datetime is not None)


def test_format_plot():
    assert (utils.format_plot('line1', 'line2') == 'line1\n\nline2')
