import os

import pytest

from django.core.urlresolvers import reverse

from rstview import parser


def test_ping_index(client):
    """Just pinging dummy homepage"""
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.parametrize("urlname,output_filename,writer", [
    ("sample-basic", "basic/page-html5.html", "html5"),
    ("sample-basic", "basic/page-html4.html", "html4"),
    ("sample-advanced", "advanced/page-html5.html", "html5"),
    ("sample-advanced", "advanced/page-html4.html", "html4"),
    ("sample-invalid", "invalid/page-html5.html", "html5"),
    ("sample-invalid", "invalid/page-html4.html", "html4"),
])
def test_render_basic(settings, client, urlname, output_filename, writer):
    """Checking rendered view"""
    settings.RSTVIEW_PARSER_WRITER = writer

    response = client.get(reverse(urlname))

    print response.content

    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, output_filename)
    with open(input_filepath, 'r') as fp:
        attempted = fp.read()

    assert response.status_code == 200

    assert response.content == attempted

    #assert 1 == 42
