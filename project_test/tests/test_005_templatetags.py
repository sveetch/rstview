import os

import pytest

from django.core.urlresolvers import reverse
from django.template import Context, Template

from rstview import parser
from rstview.templatetags.rstview_tags import rst_render


@pytest.mark.parametrize("urlname,output_filename,writer", [
    ("sample-tag-basic", "basic/page-html5.html", "html5"),
    ("sample-tag-basic", "basic/page-html4.html", "html4"),
    ("sample-tag-advanced", "advanced/page-html5.html", "html5"),
    ("sample-tag-advanced", "advanced/page-html4.html", "html4"),
    ("sample-tag-invalid", "invalid/page-html5.html", "html5"),
    ("sample-tag-invalid", "invalid/page-html4.html", "html4"),
])
def test_render_from_view(settings, client, urlname, output_filename, writer):
    """
    Checking rendered source through template tag inside a template

    Attempted render are exactly the same than for the view tests
    """
    settings.RSTVIEW_PARSER_WRITER = writer

    response = client.get(reverse(urlname))

    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, output_filename)
    with open(input_filepath, 'r') as fp:
        attempted = fp.read()

    assert response.status_code == 200

    assert response.content == attempted


@pytest.mark.parametrize("source,attempted,options", [
    (
        """Lorem **ipsum** salace""",
        """<p>Lorem <strong>ipsum</strong> salace</p>\n""",
        '',
    ),
    (
        """Lorem **ipsum salace""",
        ("""<p>Lorem <a href="#id1">"""
        """<span class="problematic" id="id2">**</span></a>ipsum """
        """salace</p>\n<div class="system-message" id="id1">\n"""
        """<p class="system-message-title">System Message: """
        """WARNING/2 (<tt class="docutils">&lt;string&gt;</tt>, """
        """line 1); <em><a href="#id2">backlink</a></em></p>"""
        """\nInline strong start-string without end-string."""
        """</div>\n"""),
        '',
    ),
    (
        """Lorem **ipsum salace""",
        ("""<p>Lorem <a href="#id1"><span class="problematic" id="id2">**"""
         """</span></a>ipsum salace</p>\n"""),
        """silent=True""",
    ),
    (
        """Foo\n***\nLorem **ipsum** salace""",
        ("""<section id="foo"><h1>Foo</h1>\n"""
        """<p>Lorem <strong>ipsum</strong> salace</p>\n"""
        """</section>"""),
        """config='full_page'""",
    ),
    (
        """Foo\n***\nLorem **ipsum salace""",
        ("""<section id="foo"><h1>Foo</h1>\n"""
        """<p>Lorem <a href="#id1"><span class="problematic" id="id2">**"""
        """</span></a>ipsum salace</p>\n"""
        """</section>"""),
        """config='full_page' silent=True""",
    ),
])
def test_render_from_template(settings, source, attempted, options):
    """Testing templatetag arguments is correctly managed"""
    # Use the tag from direct template render with computed options
    tpl = ("""{{% load rstview_tags %}}{{% rst_render doc_source """
           """{options} %}}""").format(options=options)

    # Render template
    template = Template(tpl)
    context = Context({"doc_source": source})
    rendered = template.render(context)

    assert rendered == attempted
