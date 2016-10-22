# -*- coding: utf-8 -*-
"""
Parser
======

Some helpers around **docutils** parser to easily parse reStructuredText markup
with some options.

Note:
    This module try to load the pygment directive if available, so you don't
    need to load it from your code if you want to use Pygment to highlight code
    blocks.
"""
import copy

from django.conf import settings
from django.utils.encoding import smart_str

from docutils import utils
from docutils.utils import error_reporting
from docutils.core import publish_parts

from rstview.html5writer import SemanticHTML5Writer
from rstview.registry import rstview_registry


# Safely try to load and register directive if Pygments is installed
try:
    import rstview.directives.pygments_directive  # noqa: F401
except ImportError:
    pass


# Store some methods we may need to monkeypatch during parsing (sic), so we
# mirror it to safely turn back to them.
_original_docutils_system_message = utils.Reporter.system_message
_original_docutils_output_write = error_reporting.ErrorOutput.write


class RstBasicRenderer(object):
    """
    Basic interface around **docutils** to parse and render reStructuredText
    markup.

    This follows the legacy behaviors of **docutils** parser, that means:

    * Parser errors and warnings are inserted inside the rendered source;
    * Errors and warnings are pushed to the standard output;

    Example:
        .. sourcecode:: python
            :linenos:

            >>> from rstview.parser import RstBasicRenderer
            >>> renderer = RstBasicRenderer()
            >>> renderer.parse("Lorem **ipsum** salace")
            <p>Lorem <strong>ipsum</strong> salace</p>
    """
    def __init__(self, *args, **kwargs):
        pass

    def get_options(self, name, initial_header_level=None,
                    silent=settings.RSTVIEW_PARSER_SILENT):
        """
        Load the given configuration and possibly update parameters with
        given keyword arguments.

        Args:
            name (string): Configuration name from registered configurations.

        Keyword Arguments:
            initial_header (int): To modify option ``initial_header_level``.
            silent (string): If ``True``, will push the parser reporter level
                to the lowest verbosiy so errors and warnings are ignored.
                Default value is the same as
                ``settings.RSTVIEW_PARSER_SILENT``.

        Returns:
            dict: Options to give to Docutils parser.
        """
        # Avoid to tamper settings using a deepcopy
        parser_settings = copy.deepcopy(
            rstview_registry.get_parameters(name)
        )

        if silent:
            parser_settings.update({'report_level': 5})

        if initial_header_level:
            parser_settings['initial_header_level'] = initial_header_level

        parser_settings.update(settings.RSTVIEW_PARSER_SECURITY)
        return parser_settings

    def get_writer_option(self):
        """
        Get the writer option for parser config depending it's ``html4`` or
        ``html5``.

        Returns:
            dict: A dict containing the right writer option name and value.
        """
        if settings.RSTVIEW_PARSER_WRITER == 'html5':
            return {
                'writer': SemanticHTML5Writer(),
            }
        else:
            return {
                'writer_name': "html4css1",
            }

    def parse(self, source, setting_key="default", body_only=True, **kwargs):
        """
        Parse reStructuredText source with given options.

        Args:
            source (string): reStructuredText source to parse.
            **kwargs: Arbitrary keyword arguments to give as options to
                ``RstBasicRenderer.get_options()``.

        Keyword Arguments:
            setting_key (string): Configuration name from registered
                configurations.
            body_only (string): If ``True``, parser will only return the
                rendered content else it will return the full dict from
                Docutils parser. This dict contains many datas about parsing.
                Default is ``True``.

        Returns:
            string or dict: Depending from ``body_only``, it will be a rendered
            content as a string or a dict containing datas about parsing
            (rendered content, styles, messages, title, etc..).
        """
        opts = {
            'source': smart_str(source),
            'settings_overrides': self.get_options(setting_key, **kwargs),
        }

        # Switch between html4/html5 writer
        opts.update(self.get_writer_option())

        parts = publish_parts(**opts)

        if body_only:
            return parts['fragment']

        return parts


class RstExtendedRenderer(RstBasicRenderer):
    """
    Extended interface for next generation usage.

    This promotes some extended behaviors:

    * Parser can be used to validate markup out of rendered document;
    * Nothing is printed out on standard output;

    **docutils** parser is a bit touchy to use programatically, so we need to
    apply some monkey patchs before and after parsing.

    Example:
        .. sourcecode:: python
            :linenos:

            >>> from rstview.parser import RstExtendedRenderer
            >>> renderer = RstExtendedRenderer()
            >>> renderer.parse("Lorem **ipsum** salace")
            <p>Lorem <strong>ipsum</strong> salace</p>
            >>> rendered.is_valid()
            True
            >>> rendered.get_messages()
            []
    """
    def is_valid(self):
        """
        Only to be used after parsing

        Returns:
            bool: True if no errors, else False
        """
        return not(self.messages)

    def format_parsing_error(self, error):
        """
        Format error message datas to a message line.

        Args:
            error (tuple): Message error returned by reporter contain four
                elements: line number, error code and message.

        Returns:
            string: Formatted message.
        """
        lineno, code, message = error

        return settings.RSTVIEW_ERROR_TEMPLATE.format(
            code=code,
            lineno=lineno,
            message=message
        )

    def parse(self, *args, **kwargs):
        """
        Proceed to parsing for validation

        We apply *monkey patchs* on two **docutils** methods, parse source then
        *unmonkey*.

        Everytime validation is processed, messages are reseted so it should
        be safe enough to use the RstExtendedRenderer instance for many
        documents.

        Once done you can access raw error messages datas from instance
        attribute ``messages`` or use ``RstExtendedRenderer.get_messages`` to
        have formatted message lines.

        Returns:
            string or dict: Depending from ``body_only``, it will be a rendered
            content as a string or a dict containing datas about parsing
            (rendered content, styles, messages, title, etc..).
        """
        # Ensure the list is cleaned before each validation
        self.messages = []

        def system_message(instance, level, message, *children, **kwargs):
            # Instance original method else nodes are bugged
            result = _original_docutils_system_message(instance, level,
                                                       message, *children,
                                                       **kwargs)
            # Store any warnings/erros in a global list so they can be used out
            # of rendered document
            if level >= instance.WARNING_LEVEL:
                self.messages.append((
                    kwargs.get('line', None),
                    level,
                    message
                ))

            return result

        def dummy_write(instance, data):
            """
            Don't write anything on output stream
            """
            pass

        # Monkeypatch docutils for simple errors/warnings output support
        utils.Reporter.system_message = system_message
        # Monkeypatch docutils for real silent errors/warnings (no print on std
        # output)
        error_reporting.ErrorOutput.write = dummy_write

        result = super(RstExtendedRenderer, self).parse(*args, **kwargs)

        # Unmonkey
        utils.Reporter.system_message = _original_docutils_system_message
        error_reporting.ErrorOutput.write = _original_docutils_output_write

        return result

    def get_messages(self):
        """
        Get a list of formatted messages

        Returns:
            A list of messages.
        """
        return map(self.format_parsing_error, self.messages)


def build_output(source, output_filepath, **kwargs):
    """
    Very basic shortcut helper to build a file from rendered reStructuredText
    source.

    Args:
        source (string): reStructuredText source to parse and render.
        output_filepath (string): File path where to write rendered source.
        **kwargs: Arbitrary keyword arguments to give as options to
            ``rstview.parser.SourceParser``.
    """
    render = RstBasicRenderer().parse(source, **kwargs)

    with open(output_filepath, 'w') as fp:
        fp.write(render)
