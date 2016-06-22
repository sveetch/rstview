import pytest

from django.conf import settings

from rstview import parser

#get_functional_settings(setting_key, body_only=True, initial_header_level=None, silent=True)


def test_wrong_setting():
    """Test wrong settings key name (does not exist in settings)"""
    with pytest.raises(KeyError):
        parser.get_functional_settings('nope')


def test_compute_settings_nopts():
    """Test computing settings with no options"""
    computed_settings = parser.get_functional_settings('default')

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get('default')
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    legacy_settings.update({
        'report_level': 5,
    })

    assert computed_settings == legacy_settings


def test_compute_settings_no_silent():
    """Test computing settings with silent options"""
    computed_settings = parser.get_functional_settings('default', silent=False)

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get('default')
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    assert computed_settings == legacy_settings


def test_compute_settings_header():
    """Test computing settings with initial_header_level options"""
    computed_settings = parser.get_functional_settings('default', initial_header_level=5)

    legacy_settings = settings.RSTVIEW_PARSER_FILTER_SETTINGS.get('default')
    legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    legacy_settings.update({
        'initial_header_level': 5,
    })

    assert computed_settings == legacy_settings

    #assert 1 == 42
