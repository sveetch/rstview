import pytest

from django.core.urlresolvers import reverse


def test_ping_index(admin_client):
    """Just dummy ping on homepage"""
    response = admin_client.get(reverse('home'))
    assert response.status_code == 200
