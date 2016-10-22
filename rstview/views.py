# -*- coding: utf-8 -*-
"""

.. _views-intro:

Views
=====

"""
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe

from rstview import parser


class RstViewInvalidException(Exception):
    """
    Exception to be raised when RSTFileView usage is incorrect.
    """
    pass


class RSTFileView(TemplateView):
    """
    Parse and render a reStructuredText file from given path.

    Example:

        .. sourcecode:: python

            from django.conf.urls import url

            from rstview.views import RSTFileView

            urlpatterns = [
                url(r'^basic/$', RSTFileView.as_view(
                    doc_path="/home/foo/basic/input.rst",
                    doc_title="Basic sample"
                ), name='sample-view-basic'),
            ]

    Attributes:
        template_name (string): Template file to render. Default to
            ``rstview/fileview.html``.
        doc_title (string): Optionnal document title. Default to ``None``.
        doc_path (string): Path to a reStructuredText file, it is recommended
            you use an absolute path.

            This is the only required argument you must allways define.

            Default to ``None``.
        doc_parser_class (object): A parser class from ``rstview.parser``.
            Default is ``rstview.parser.RstExtendedRenderer``.
        doc_parser_silent (bool): Enable to override default *silent mode*
            behavior. Default value is the same as
            ``settings.RSTVIEW_PARSER_SILENT``.
        doc_parser_bodyonly (bool): If ``True``, parser will only return the
            rendered content, this is the default behavior. Default is
            ``False``.
        doc_parser_configuration (string): A registered configuration name.
            Default to ``default``.
    """
    #: Default template
    template_name = "rstview/fileview.html"
    doc_title = None
    doc_path = None
    doc_parser_class = parser.RstExtendedRenderer
    doc_parser_silent = settings.RSTVIEW_PARSER_SILENT
    doc_parser_bodyonly = True
    doc_parser_configuration = 'default'

    def get_document_title(self):
        """
        Get document title from ``RSTFileView.doc_title``

        Returns:
            string: Document title.
        """
        return self.doc_title

    def get_parser_opts(self):
        """
        Return parser options.

        Returns:
            dict: Options to give to ``parser.SourceParser``:

                * ``setting_key``: from class attribute
                  ``RSTFileView.doc_parser_configuration``;
                * ``silent``: from class attribute
                  ``RSTFileView.doc_parser_silent``;
                * ``body_only``: from class attribute
                  ``RSTFileView.doc_parser_bodyonly``;
        """
        return {
            'setting_key': self.doc_parser_configuration,
            'silent': self.doc_parser_silent,
            'body_only': self.doc_parser_bodyonly,
        }

    def get_source(self):
        """
        Return file source from given path in ``RSTFileView.doc_path``.

        Raises:
            rstview.views.RstViewInvalidException: If ``RSTFileView.doc_path``
                is not defined.

        Returns:
            string: File content.
        """
        if not self.doc_path:
            raise RstViewInvalidException(("RSTFileView.doc_path must be "
                                          "defined"))

        with open(self.doc_path, 'r') as fp:
            source = fp.read()
        return source

    def render_source(self, source):
        """
        Parse given source and return result as safe for django template.

        Use ``RSTFileView.get_parser_opts()`` to get and give options to
        parser.

        Args:
            source (string): reStructuredText markup to parse.

        Returns:
            string: Rendered source from parser.
        """
        parser = self.doc_parser_class()
        output = parser.parse(source, **self.get_parser_opts())

        return mark_safe(output)

    def get_context_data(self, **kwargs):
        """
        Expand template context with some document related variables:

        doc_title
            The given document title.
        doc_source
            Source from given filepath.
        doc_html
            Rendered source from parser.
        doc_parser_configuration
            Used configuration name.

        Returns:
            dict: Context variables expanded with variables.
        """
        context = super(RSTFileView, self).get_context_data(**kwargs)

        source = self.get_source()
        rendered = self.render_source(source)

        context.update({
            'doc_title': self.get_document_title(),
            'doc_source': source,
            'doc_html': rendered,
            'doc_parser_configuration': self.doc_parser_configuration,
        })
        return context
