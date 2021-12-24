import lib.plugin as plugin


def test_add_live_schedule_menu_item():
    assert (plugin.add_live_schedule_menu_item() is True)


def test_get_live_schedule_index():
    assert (plugin.live_schedule_index() is True)
