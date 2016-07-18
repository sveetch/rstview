"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic.base import TemplateView

from rstview.views import RSTFileView


def getsourcepath(filename):
    """Shortcut for absolute path to a test fixture file"""
    return os.path.join(settings.TESTS_FIXTURES_DIR, filename)


urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),

    # Dummy homepage just for simple ping view
    url(r'^$', TemplateView.as_view(
        template_name="homepage.html"
    ), name='home'),

    # Some views using ``rstview.views.RSTFileView``
    url(r'^basic/$', RSTFileView.as_view(
        doc_path=getsourcepath("basic/input.rst"),
        doc_title="Basic sample"
    ), name='sample-basic'),
    url(r'^advanced/$', RSTFileView.as_view(
        doc_path=getsourcepath("advanced/input.rst"),
        doc_title="Advanced sample"
    ), name='sample-advanced'),
    url(r'^invalid/$', RSTFileView.as_view(
        doc_path=getsourcepath("invalid/input.rst"),
        doc_title="Invalid sample"
    ), name='sample-invalid'),
]
