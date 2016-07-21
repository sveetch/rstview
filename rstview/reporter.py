# -*- coding: utf-8 -*-
"""
Parser reporter
===============

Custom reporter to validate source without rendering the parser result.

This is especially useful to validate submitted reStructuredText content from
a form.
"""
import docutils

from django.conf import settings


def format_parsing_errors(error):
    """
    Format an error line returned by reporter.

    Args:
        error (tuple): Message error returned by reporter contain four
            elements: error code, message, content and source.

    Returns:
        string: Formatted message.
    """
    code, message, content, source = error

    return settings.RSTVIEW_ERROR_TEMPLATE.format(
        code=code,
        source=source,
        lineno=source.get('line', 0),
        message=message
    )


class SilentReporter(docutils.utils.Reporter):
    """
    Silent reporter catch and memorize all warnings and errors so they can be
    used subsequently through the reporter instance.

    Attempt the same arguments than inherited ``docutils.utils.Reporter``.
    """
    def __init__(self, source, report_level, halt_level, stream=None,
                 debug=0, encoding='ascii', error_handler='replace'):
        self.messages = []
        docutils.utils.Reporter.__init__(self, source, report_level,
                                         halt_level, stream, debug, encoding,
                                         error_handler)

    def system_message(self, level, message, *children, **kwargs):
        self.messages.append((level, message, children, kwargs))


def SourceReporter(source, setting_key="default"):
    """
    Helper to use silent reporter that is able to validate reStructuredText
    markup from a source and return errors and warnings from parser.

    This effectively parse a source but only to validate it, no parsing render
    is returned.

    Todo:
        This stop parsing since first occured errors, would be nicer to
        continue parsing to return every errors in one time. (Third party
        tool using reporter would appreciate this for better user experience
        to be able to fix every error in one shot);

    Args:
        source (string): reStructuredText source to parse.

    Keyword Arguments:
        setting_key (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.

    Returns:
        list: Reporter messages if any error have been encountered during
        parsing.
    """
    source_path = None

    parser = docutils.parsers.rst.Parser()

    opts = docutils.frontend.OptionParser().get_default_values()
    opts.tab_width = 4
    opts.pep_references = None
    opts.rfc_references = None

    reporter = SilentReporter(
        source_path,
        opts.report_level,
        opts.halt_level,
        stream=opts.warning_stream,
        debug=opts.debug,
        encoding=opts.error_encoding,
        error_handler=opts.error_encoding_error_handler
    )

    document = docutils.nodes.document(opts, reporter, source=source_path)
    document.note_source(source_path, -1)
    try:
        parser.parse(source, document)
    except AttributeError:
        pass
    except TypeError:
        # Catch ``TypeError`` to avoid problems with local roles
        # NOTE: Is this still necessary ?
        pass
    return reporter.messages
