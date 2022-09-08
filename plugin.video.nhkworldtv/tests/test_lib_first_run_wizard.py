from lib import first_run_wizard


def test_run_wizard():
    # Test if a Episode is returned
    assert first_run_wizard.show_wizard() is True
