# -*- coding: utf-8 -*-
"""
Parser helpers
==============

Some helpers around Docutils parser to easily parse reStructuredText markup
with some options.

Note:
    This module try to load the pygment directive if available, so you don't
    need to load it from your code if you want to use Pygment to highlight code
    blocks.

"""
import copy

from django.conf import settings
from django.utils.encoding import smart_str

from docutils.core import publish_parts

from rstview import html5writer


# Safely try to load and register directive if Pygments is installed
try:
    import rstview.directives.pygments_directive  # noqa: F401
except ImportError:
    pass


def get_functional_settings(setting_key, initial_header_level=None,
                            silent=True):
    """
    From given options in keyword arguments, will modify selected option
    set from given ``setting_key``.

    Args:
        setting_key (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.

    Keyword Arguments:
        initial_header_level (string): Title level available to start from. If
            ``2`` biggest title will be ``h2``, if ``3`` it will be ``h3``,
            etc..
        silent (string): If ``True``, rendered content won't include errors and
            warning. Default is ``True``.

    Returns:
        dict: Options to give to Docutils parser.
    """
    parser_settings = copy.deepcopy(
        settings.RSTVIEW_PARSER_FILTER_SETTINGS[setting_key]
    )
    parser_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    if silent:
        parser_settings.update({'report_level': 5})

    if initial_header_level:
        parser_settings['initial_header_level'] = initial_header_level

    return parser_settings


def SourceParser(source, setting_key="default", body_only=True,
                 initial_header_level=None, silent=True):
    """
    Parse reStructuredText source with given options.

    Args:
        source (string): reStructuredText source to parse.

    Keyword Arguments:
        setting_key (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
        body_only (string): If ``True``, parser will only return the rendered
            content else it will return the full dict from Docutils parser.
            This dict contains many datas about parsing. Default is ``True``.
        silent (string): If ``True``, rendered content won't include errors and
            warning. Default is ``True``.
        initial_header_level (string): Title level available to start from. If
            ``2`` biggest title will be ``h2``, if ``3`` it will be ``h3``,
            etc.. This overrides the given level from option set.

    Returns:
        string or dict: Depending from ``body_only``, it will be a rendered
        content as a string or a dict containing datas about parsing (rendered
        content, styles, messages, title, etc..).
    """
    parser_settings = get_functional_settings(setting_key,
                                              initial_header_level,
                                              silent)

    opts = {
        'source': smart_str(source),
        'settings_overrides': parser_settings,
    }

    # Switch between html4/html5 writer
    if settings.RSTVIEW_PARSER_WRITER == 'html5':
        opts['writer'] = html5writer.SemanticHTML5Writer()
    else:
        opts['writer_name'] = "html4css1"

    parts = publish_parts(**opts)

    if body_only:
        return parts['fragment']
    return parts


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
    render = SourceParser(source, **kwargs)

    with open(output_filepath, 'w') as fp:
        fp.write(render)
