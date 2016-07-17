# -*- coding: utf-8 -*-
"""
ReStructuredText parser reporter to validate a source
"""
import docutils

from django.conf import settings


def format_parsing_errors(error):
    """
    Format an error line returned by reporter

    NOTE: Previously named ``parser.map_parsing_errors``
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
    Silent reporter

    All warnings and errors will be stored and can be used subsequently through
    the reporter instance
    """
    def __init__(self, source, report_level, halt_level, stream=None,
                    debug=0, encoding='ascii', error_handler='replace'):
        self.messages = []
        docutils.utils.Reporter.__init__(self, source, report_level,
                                         halt_level, stream, debug, encoding,
                                         error_handler)

    def system_message(self, level, message, *children, **kwargs):
        self.messages.append((level, message, children, kwargs))


def SourceReporter(data, setting_key="default"):
    """
    Catch errors and syntax warnings to use them at part of the rendered
    content.

    This effectively parse a source but only to validate it, no parsing render
    is returned.

    Return a list of reporter messages if any error have been encountered
    during parsing. Should be empty if no error has occured.

    NOTE:
        * Reporter parameters may not be accurate in every situation;
        * Flaw: Stop parsing since first occured errors, would be nicer to
          continue parsing to return every errors in one time. (Third party
          tool using reporter would appreciate this for better user experience
          to be able to fix every error in one shot);
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
        parser.parse(data, document)
    except AttributeError:
        pass
    except TypeError:
        # Catch ``TypeError`` to avoid problems with local roles
        # NOTE: Is this still necessary ?
        pass
    return reporter.messages
