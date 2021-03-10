import lib.plugin as plugin


def test_main_menu():
    assert (plugin.index() is True)


def test_vod_menu_get_programs():
    detail_url = plugin.vod_programs()
    assert (detail_url is not None)


def test_vod_menu__get_categories():
    detail_url = plugin.vod_categories()
    print(detail_url)
    assert (detail_url is not None)


def test_vod_menu_get_playlists():
    detail_url = plugin.vod_playlists()
    print(detail_url)
    assert (detail_url is not None)


def test_vod_menu():
    assert (plugin.vod_index() is True)


# At a glance


def test_add_ataglance_menu_item():
    assert (plugin.add_ataglance_menu_item() is True)


def test_get_ataglance_index():
    assert (plugin.ataglance_index() is True)


# Top stories


def test_add_topstories_menu_item():
    assert (plugin.add_topstories_menu_item() is True)


def test_get_topstories_index():
    assert (plugin.topstories_index() is True)


# News programs


def test_get_news_programs_index():
    assert (plugin.news_programs_index() is True)
