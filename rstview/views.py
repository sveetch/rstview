# -*- coding: utf-8 -*-
"""
Views
=====

"""
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe

from rstview import parser


class RSTFileView(TemplateView):
    """
    Parse and render a reStructuredText file from given path.

    **Usage:**

        .. sourcecode:: python

            from django.conf.urls import url

            from rstview.views import RSTFileView

            urlpatterns = [
                url(r'^basic/$', RSTFileView.as_view(
                    doc_path="/home/foo/basic/input.rst",
                    doc_title="Basic sample"
                ), name='sample-view-basic'),
            ]
    """
    #: Default template
    template_name = "rstview/fileview.html"
    doc_title = None
    doc_path = None
    doc_parser_silent = False
    doc_parser_bodyonly = True
    doc_parser_opts_name = 'default'

    def get_document_title(self, **kwargs):
        """Return document title from ``RSTFileView.doc_title``"""
        return self.doc_title

    def get_parser_opts(self, **kwargs):
        """
        Return parser options from class attributes:

        doc_parser_opts_name
            Name of an option set from
            ``rstview.settings.RSTVIEW_PARSER_FILTER_SETTINGS``. Default used
            name is ``default``.
        doc_parser_silent
            If ``True``, parser won't include errors and warning in rendered
            source. Default is ``False``.
        doc_parser_bodyonly
            If ``True``, parser will only return the rendered content, this
            is the default behavior.
        """
        return {
            'setting_key': self.doc_parser_opts_name,
            'silent': self.doc_parser_silent,
            'body_only': self.doc_parser_bodyonly,
        }

    def get_source(self):
        """Return file source from given path in ``RSTFileView.doc_path``"""
        with open(self.doc_path, 'r') as fp:
            source = fp.read()
        return source

    def render_source(self, source, **kwargs):
        """Parse given source and return result as safe for django template"""
        output = parser.SourceParser(source, **self.get_parser_opts())

        return mark_safe(output)

    def get_context_data(self, **kwargs):
        """
        Template context will be expanded with some document related
        variables:

        doc_title
            The given document title.
        doc_source
            Source from given filepath.
        doc_html
            Rendered source from parser.
        doc_parser_opts_name
            Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
        """
        context = super(RSTFileView, self).get_context_data(**kwargs)

        source = self.get_source()
        rendered = self.render_source(source, **kwargs)

        context.update({
            'doc_title': self.get_document_title(**kwargs),
            'doc_source': source,
            'doc_html': rendered,
            'doc_parser_opts_name': self.doc_parser_opts_name,
        })
        return context
