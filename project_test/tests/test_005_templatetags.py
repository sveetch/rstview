import os

import pytest

from django.core.urlresolvers import reverse

from rstview import parser

"""
TODO: changing tag options
"""

@pytest.mark.parametrize("urlname,output_filename,writer", [
    ("sample-tag-basic", "basic/page-html5.html", "html5"),
    ("sample-tag-basic", "basic/page-html4.html", "html4"),
    ("sample-tag-advanced", "advanced/page-html5.html", "html5"),
    ("sample-tag-advanced", "advanced/page-html4.html", "html4"),
    ("sample-tag-invalid", "invalid/page-html5.html", "html5"),
    ("sample-tag-invalid", "invalid/page-html4.html", "html4"),
])
def test_render_basic(settings, client, urlname, output_filename, writer):
    """
    Checking rendered source through template tag

    Attempted render is the exactly the same than for the view tests
    """
    settings.RSTVIEW_PARSER_WRITER = writer

    response = client.get(reverse(urlname))

    #print response.content

    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, output_filename)
    with open(input_filepath, 'r') as fp:
        attempted = fp.read()

    assert response.status_code == 200

    assert response.content == attempted
