# -*- coding: utf-8 -*-
"""
ReStructuredText parser facilities
"""
import copy

from django.conf import settings
from django.utils.encoding import smart_str

import docutils

from rstview import html5writer


# Loading directive with failsafe if Pygments is not installed
try:
    import rstview.directives.pygments_directive
except ImportError:
    pass


def get_functional_settings(setting_key, initial_header_level=None, silent=True):
    """
    Compute various parser settings and options to return an unique settings dict
    """
    parser_settings = copy.deepcopy(settings.RSTVIEW_PARSER_FILTER_SETTINGS[setting_key])
    parser_settings.update(settings.RSTVIEW_PARSER_SECURITY)

    if silent:
        parser_settings.update({'report_level': 5})

    if initial_header_level:
        parser_settings['initial_header_level'] = initial_header_level

    return parser_settings


def SourceParser(source, setting_key="default", body_only=True, initial_header_level=None, silent=True):
    """
    Parse the source with the given options and settings
    """
    parser_settings = get_functional_settings(setting_key, initial_header_level, silent)

    # Switch between xhtml (aka html4css1 in docutils) and custom html5 writer
    if settings.RSTVIEW_PARSER_WRITER == 'html5':
        parts = docutils.core.publish_parts(source=smart_str(source), writer=html5writer.SemanticHTML5Writer(), settings_overrides=parser_settings)
    else:
        parts = docutils.core.publish_parts(source=smart_str(source), writer_name="html4css1", settings_overrides=parser_settings)

    if body_only:
        return parts['fragment']
    return parts
