import os

import pytest

from django.core.urlresolvers import reverse

from rstview.views import RstViewInvalidException


def test_ping_index(client):
    """Just pinging dummy homepage"""
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.parametrize("urlname,output_filename,writer", [
    ("sample-view-basic", "basic/page-html5.html", "html5"),
    ("sample-view-basic", "basic/page-html4.html", "html4"),
    ("sample-view-advanced", "advanced/page-html5.html", "html5"),
    ("sample-view-advanced", "advanced/page-html4.html", "html4"),
    ("sample-view-invalid", "invalid/page-html5.html", "html5"),
    ("sample-view-invalid", "invalid/page-html4.html", "html4"),
])
def test_render_basic(settings, client, urlname, output_filename, writer):
    """Checking rendered source through view"""
    settings.RSTVIEW_PARSER_WRITER = writer

    response = client.get(reverse(urlname))

    #print response.content

    input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, output_filename)
    with open(input_filepath, 'r') as fp:
        attempted = fp.read()

    assert response.status_code == 200

    assert response.content == attempted

    #assert 1 == 42


def test_empty_doc_path(settings, client):
    """Empty doc_path class attribute raise an exception"""
    with pytest.raises(RstViewInvalidException):
        response = client.get(reverse('sample-view-error'))
