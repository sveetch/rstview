"""
TODO: Lack of tests with encoding issues (unicode, etc..)
"""
import os

import pytest

from rstview import parser


def test_parser_basic_content(settings):
    """Parse a basic input with default writer (html5) and returned body"""
    source = """Lorem **ipsum** salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=True,
                                 initial_header_level=None, silent=False)
    assert render == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""


def test_parser_no_body_only(settings):
    """Parse a basic input and returned whole resulted dict from parser"""
    source = """Lorem **ipsum** salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=False,
                                 initial_header_level=None, silent=True)

    # Does we have a returned dict (instead of string with body_only==True)
    assert type(render) == dict

    # Check some fields exists in returned Dict
    fields = ['version', 'encoding', 'html_title', 'title', 'html_body',
              'body', 'footer', 'whole']
    for f in fields:
        assert (f in render.keys()) == True

    # Check the body field is ok
    assert render['body'] == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""


def test_parser_invalid_syntax_silent(settings):
    """Parse a basic invalid input with silent mode enabled"""
    source = """Lorem **ipsum salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=True,
                                 initial_header_level=None, silent=True)

    assert render == ("""<p>Lorem <a href="#id1">"""
                      """<span class="problematic" id="id2">**</span></a>ipsum """
                      """salace</p>\n""")


def test_parser_invalid_syntax_nosilent(settings):
    """Parse a basic invalid input with silent mode disabled"""
    source = """Lorem **ipsum salace"""
    render = parser.SourceParser(source, setting_key="default", body_only=True,
                                 initial_header_level=None, silent=False)

    assert render == ("""<p>Lorem <a href="#id1">"""
                      """<span class="problematic" id="id2">**</span></a>ipsum """
                      """salace</p>\n<div class="system-message" id="id1">\n"""
                      """<p class="system-message-title">System Message: """
                      """WARNING/2 (<tt class="docutils">&lt;string&gt;</tt>, """
                      """line 1); <em><a href="#id2">backlink</a></em></p>"""
                      """\nInline strong start-string without end-string."""
                      """</div>\n""")


@pytest.mark.parametrize("source_filename,output_filename,writer", [
    ("basic/input.rst", "basic/output-html5.html", "html5"),
    ("basic/input.rst", "basic/output-html4.html", "html4"),
    ("advanced/input.rst", "advanced/output-html5.html", "html5"),
    ("advanced/input.rst", "advanced/output-html4.html", "html4"),
    ("invalid/input.rst", "invalid/output-html5.html", "html5"),
    ("invalid/input.rst", "invalid/output-html4.html", "html4"),
])
def test_parser_file(settings, storageparameters, source_filename, output_filename, writer):
    """Compare a rendered source to attempted return from a data fixture file"""
    # Temporary change the writer
    settings.RSTVIEW_PARSER_WRITER = writer

    input_filepath = os.path.join(storageparameters.fixtures_path, source_filename)
    output_filepath = os.path.join(storageparameters.fixtures_path, output_filename)

    with open(input_filepath, 'r') as fp:
        source = fp.read()

    with open(output_filepath, 'r') as fp:
        attempted = fp.read()

    # Temporary
    #parser.build_output(source, output_filepath, setting_key="default",
                #body_only=True, initial_header_level=None,
                #silent=False)

    render = parser.SourceParser(source, setting_key="default", body_only=True,
                                 initial_header_level=None, silent=False)

    assert render == attempted
