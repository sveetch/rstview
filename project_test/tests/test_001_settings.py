import copy

import pytest

from rstview.parser import RstBasicRenderer


def test_wrong_setting(settings):
    """Test wrong settings key name (does not exist in settings)"""
    with pytest.raises(KeyError):
        RstBasicRenderer().get_options('nope')


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_silent(settings, setting_key):
    """Computing settings with no options"""
    computed_settings = RstBasicRenderer().get_options(setting_key, silent=True)

    legacy_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key))
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    # When silent=True (default)
    legacy_settings.update({
        'report_level': 5,
    })

    assert computed_settings == legacy_settings


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_no_silent(settings, setting_key):
    """Computing settings with silent options"""
    computed_settings = RstBasicRenderer().get_options(setting_key)

    legacy_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key))
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    assert computed_settings == legacy_settings


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_header(settings, setting_key):
    """Computing settings with initial_header_level options"""
    computed_settings = RstBasicRenderer().get_options(setting_key, initial_header_level=5)

    legacy_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key))
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    # Other level than the default one
    legacy_settings.update({
        'initial_header_level': 5,
    })

    assert computed_settings == legacy_settings

    #assert 1 == 42
