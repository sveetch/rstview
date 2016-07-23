"""
TODO: Lack of tests with encoding issues (unicode, etc..)
"""
import os

import pytest

from rstview.parser import RstBasicRenderer, RstExtendedRenderer, build_output


def test_parser_basic_content(settings):
    """Parse a basic input with default options"""
    source = """Lorem **ipsum** salace"""

    render = RstBasicRenderer().parse(source)

    assert render == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""


def test_parser_no_body_only(settings):
    """Parse a basic input and returned whole resulted dict from parser"""
    source = """Lorem **ipsum** salace"""

    render = RstBasicRenderer().parse(source, **{
        'body_only': False,
    })

    # Does we have a returned dict (instead of string with body_only==True)
    assert type(render) == dict

    # Check some fields exists in returned Dict
    fields = ['version', 'encoding', 'html_title', 'title', 'html_body',
              'body', 'footer', 'whole']
    for f in fields:
        assert (f in render.keys()) == True

    # Check the body field is ok
    assert render['body'] == """<p>Lorem <strong>ipsum</strong> salace</p>\n"""


def test_parser_invalid_syntax_silent(settings, capsys):
    """Parse a basic invalid input with silent mode enabled"""
    source = """Lorem **ipsum salace"""

    render = RstBasicRenderer().parse(source, **{
        'silent': True,
    })

    out, err = capsys.readouterr()

    # Ensure parser is totally silent
    assert out == ""
    assert err == ""

    assert render == ("""<p>Lorem <a href="#id1">"""
                      """<span class="problematic" id="id2">**</span></a>ipsum """
                      """salace</p>\n""")


def test_parser_invalid_syntax_nosilent(settings, capsys):
    """Parse a basic invalid input with silent mode disabled"""
    source = """Lorem **ipsum salace"""

    render = RstBasicRenderer().parse(source)

    out, err = capsys.readouterr()

    # Ensure parser is totally silent
    assert out == ""
    assert err == ("""<string>:1: (WARNING/2) Inline strong start-string """
                   """without end-string.\n""")

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
    ("invalid-2/input.rst", "invalid-2/output-html5.html", "html5"),
    ("invalid-2/input.rst", "invalid-2/output-html4.html", "html4"),
])
def test_parser_file_nosilent(settings, storageparameters, source_filename,
                              output_filename, writer):
    """Compare a rendered source to attempted return from a data fixture file"""
    # Temporary change the writer
    settings.RSTVIEW_PARSER_WRITER = writer

    input_filepath = os.path.join(storageparameters.fixtures_path, source_filename)
    output_filepath = os.path.join(storageparameters.fixtures_path, output_filename)

    with open(input_filepath, 'r') as fp:
        source = fp.read()

    ## Temporary
    #build_output(source, output_filepath)

    with open(output_filepath, 'r') as fp:
        attempted = fp.read()

    render = RstBasicRenderer().parse(source)

    assert render == attempted


def test_validate_basic_content(settings):
    """Validate a basic valid input"""
    source = """Lorem **ipsum** salace"""

    renderer = RstExtendedRenderer()
    renderer.parse(source)

    assert renderer.is_valid() == True

    assert renderer.messages == []


def test_validate_invalid_syntax(settings, capsys):
    """Validate a basic invalid input"""
    source = """Lorem **ipsum salace"""

    renderer = RstExtendedRenderer()
    renderer.parse(source)

    out, err = capsys.readouterr()

    assert renderer.is_valid() == False

    # Ensure parser is totally silent
    assert out == ""
    assert err == ""

    assert renderer.messages == [
        (1, 2, 'Inline strong start-string without end-string.'),
    ]


def test_validate_invalid2_syntax(settings, capsys):
    """Validate another basic invalid input"""
    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, "invalid-2/input.rst")
    with open(input_filepath, 'r') as fp:
        source = fp.read()

    renderer = RstExtendedRenderer()
    renderer.parse(source)

    out, err = capsys.readouterr()

    assert renderer.is_valid() == False

    # Ensure parser is totally silent
    assert out == ""
    assert err == ""

    assert renderer.messages == [
        (1, 2, 'Inline strong start-string without end-string.'),
        (8, 2, 'Inline strong start-string without end-string.'),
        (8, 2, 'Inline strong start-string without end-string.'),
        (8, 2, 'Inline emphasis start-string without end-string.'),
        (31, 2, 'Inline literal start-string without end-string.'),
    ]


def test_validate_invalid2_syntax_formatted(settings, capsys):
    """Validate another basic invalid input but with formatted messages"""
    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, "invalid-2/input.rst")
    with open(input_filepath, 'r') as fp:
        source = fp.read()

    renderer = RstExtendedRenderer()
    renderer.parse(source)

    out, err = capsys.readouterr()

    assert renderer.is_valid() == False

    # Ensure parser is totally silent
    assert out == ""
    assert err == ""

    assert renderer.get_messages() == [
        u'Line 1 : Inline strong start-string without end-string.',
        u'Line 8 : Inline strong start-string without end-string.',
        u'Line 8 : Inline strong start-string without end-string.',
        u'Line 8 : Inline emphasis start-string without end-string.',
        u'Line 31 : Inline literal start-string without end-string.'
    ]
