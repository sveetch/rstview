import pytest

from rstview import parser


def test_wrong_setting(settings):
    """Test wrong settings key name (does not exist in settings)"""
    with pytest.raises(KeyError):
        parser.get_functional_settings('nope')


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_nopts(settings, setting_key):
    """Test computing settings with no options"""
    computed_settings = parser.get_functional_settings(setting_key)

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key)
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    # When silent=True (default)
    legacy_settings.update({
        'report_level': 5,
    })

    assert computed_settings == legacy_settings


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_no_silent(settings, setting_key):
    """Test computing settings with silent options"""
    computed_settings = parser.get_functional_settings(setting_key, silent=False)

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key)
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    assert computed_settings == legacy_settings


@pytest.mark.parametrize("setting_key", ["default", "full_page"])
def test_compute_settings_header(settings, setting_key):
    """Test computing settings with initial_header_level options"""
    computed_settings = parser.get_functional_settings(setting_key, initial_header_level=5)

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key)
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    # Other level than the default one
    legacy_settings.update({
        'initial_header_level': 5,
    })

    assert computed_settings == legacy_settings

    #assert 1 == 42
