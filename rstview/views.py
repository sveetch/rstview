# -*- coding: utf-8 -*-
"""
ReStructuredText views
"""
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe

from rstview import parser


class RSTFileView(TemplateView):
    """
    View to display a ReST file

    Open given source filepath, parse it and render it.

    Context will be expanded from some document related variables:

    doc_title
        The given document title.
    doc_source
        Source from given filepath.
    doc_html
        Rendered source from parser.
    doc_parser_opts_name
        Key name of parser options from
        ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
    """
    template_name = "rstview/fileview.html"
    doc_title = None
    doc_path = None
    doc_parser_silent = False
    doc_parser_bodyonly = True
    doc_parser_opts_name = 'default'

    def get_document_title(self, **kwargs):
        """Return document title from RSTFileView.doc_title"""
        return self.doc_title

    def get_parser_opts(self, **kwargs):
        """Return parser options"""
        return {
            'setting_key': self.doc_parser_opts_name,
            'silent': self.doc_parser_silent,
            'body_only': self.doc_parser_bodyonly,
        }

    def get_source(self, **kwargs):
        """Return file content"""
        with open(self.doc_path, 'r') as fp:
            source = fp.read()
        return source

    def render_source(self, source, **kwargs):
        """Parse given source and return result as safe for django template"""
        output = parser.SourceParser(source, **self.get_parser_opts())

        return mark_safe(output)

    def get_context_data(self, **kwargs):
        context = super(RSTFileView, self).get_context_data(**kwargs)

        source = self.get_source(**kwargs)
        rendered = self.render_source(source, **kwargs)

        context.update({
            'doc_title': self.get_document_title(**kwargs),
            'doc_source': source,
            'doc_html': rendered,
            'doc_parser_opts_name': self.doc_parser_opts_name,
        })
        return context
