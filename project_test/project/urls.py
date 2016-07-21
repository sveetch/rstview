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


class SourceReaderView(RSTFileView):
    """
    Dummy view to read source content from given filepath and render it
    through a template tag

    Open source file alike RSTFileView but don't do all the parser things
    """
    template_name = "templatetags_usage.html"

    def get_context_data(self, **kwargs):
        context = super(RSTFileView, self).get_context_data(**kwargs)

        context.update({
            'doc_title': self.get_document_title(),
            'doc_path': self.doc_path,
            'doc_source': self.get_source(),
        })
        return context


urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),

    # Dummy homepage just for simple ping view
    url(r'^$', TemplateView.as_view(
        template_name="homepage.html"
    ), name='home'),

    # Some views using ``rstview.views.RSTFileView``
    url(r'^view/basic/$', RSTFileView.as_view(
        doc_path=getsourcepath("basic/input.rst"),
        doc_title="Basic sample"
    ), name='sample-view-basic'),
    url(r'^view/advanced/$', RSTFileView.as_view(
        doc_path=getsourcepath("advanced/input.rst"),
        doc_title="Advanced sample"
    ), name='sample-view-advanced'),
    url(r'^view/invalid/$', RSTFileView.as_view(
        doc_path=getsourcepath("invalid/input.rst"),
        doc_title="Invalid sample"
    ), name='sample-view-invalid'),

    # Invalid RSTFileView usage that raise an error 500
    url(r'^view/empty_doc_path/$', RSTFileView.as_view(
        doc_title="Empty doc_path"
    ), name='sample-view-error'),

    # Views to render source from template tag
    url(r'^templatetag/basic/$', SourceReaderView.as_view(
        doc_path=getsourcepath("basic/input.rst"),
        doc_title="Basic sample"
    ), name='sample-tag-basic'),
    url(r'^templatetag/advanced/$', SourceReaderView.as_view(
        doc_path=getsourcepath("advanced/input.rst"),
        doc_title="Advanced sample"
    ), name='sample-tag-advanced'),
    url(r'^templatetag/invalid/$', SourceReaderView.as_view(
        doc_path=getsourcepath("invalid/input.rst"),
        doc_title="Invalid sample"
    ), name='sample-tag-invalid'),
]
