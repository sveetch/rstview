import pytest

from rstview import parser

#SourceParser(source, setting_key="default", body_only=True, initial_header_level=None, silent=True)


def test_parser_basic_content(settings):
    """Parse a very basic content"""
    source = """Lorem **ipsum** salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=True,
                                 initial_header_level=None, silent=True)
    assert render == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""


def test_parser_no_body_only(settings):
    """Test wrong settings key name (does not exist in settings)"""
    source = """Lorem **ipsum** salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=False,
                                 initial_header_level=None, silent=True)
    #print render.keys()
    #fields = ['version', 'encoding', 'html_title', 'title', 'html_body', 'body', 'footer', 'whole']

    assert render['body'] == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""

    #assert 1 == 42
