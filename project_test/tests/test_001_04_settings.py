import copy

import pytest

from rstview.parser import RstBasicRenderer
from rstview.registry import RstviewConfigNotRegistered, rstview_registry


def test_wrong_setting(settings):
    """Test wrong settings key name (does not exist in settings)"""
    with pytest.raises(RstviewConfigNotRegistered):
        RstBasicRenderer().get_options('nope')


@pytest.mark.parametrize("setting_key,attempted", [
    ("default", {
        'initial_header_level': 3,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'language_code': "en",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'report_level': 5,
        'enable_exit': 0,
        'halt_level': 6,
    }),
    ("full_page", {
        'initial_header_level': 1,
        'file_insertion_enabled': False,
        'raw_enabled': True,
        'language_code': "fr",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'report_level': 5,
        'enable_exit': 0,
        'halt_level': 6,
    }),
])
def test_compute_settings_silent(settings, setting_key, attempted):
    """Computing settings with no options"""
    computed_settings = RstBasicRenderer().get_options(setting_key, silent=True)

    assert computed_settings == attempted


@pytest.mark.parametrize("setting_key,attempted", [
    ("default", {
        'initial_header_level': 3,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'language_code': "en",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'enable_exit': 0,
        'halt_level': 6,
    }),
    ("full_page", {
        'initial_header_level': 1,
        'file_insertion_enabled': False,
        'raw_enabled': True,
        'language_code': "fr",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'enable_exit': 0,
        'halt_level': 6,
    }),
])
def test_compute_settings_no_silent(settings, setting_key, attempted):
    """Computing settings with silent options"""
    computed_settings = RstBasicRenderer().get_options(setting_key)

    #legacy_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key))
    #legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    assert computed_settings == attempted


@pytest.mark.parametrize("setting_key,attempted", [
    ("default", {
        'initial_header_level': 5,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'language_code': "en",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'enable_exit': 0,
        'halt_level': 6,
    }),
    ("full_page", {
        'initial_header_level': 5,
        'file_insertion_enabled': False,
        'raw_enabled': True,
        'language_code': "fr",
        'footnote_references': 'superscript',
        'doctitle_xform': False,
        'enable_exit': 0,
        'halt_level': 6,
    }),
])
def test_compute_settings_header(settings, setting_key, attempted):
    """Computing settings with initial_header_level options"""
    computed_settings = RstBasicRenderer().get_options(setting_key, initial_header_level=5)

    #legacy_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS.get(setting_key))
    #legacy_settings.update(settings.RSTVIEW_PARSER_SECURITY)
    ## Other level than the default one
    #legacy_settings.update({
        #'initial_header_level': 5,
    #})

    assert computed_settings == attempted
