# -*- coding: utf-8 -*-
"""
App default settings
"""
# Some docutils security settings you should not change
# They're automaticlly appended to each used settings from parser
RSTVIEW_PARSER_SECURITY = {
    'halt_level': 6,
    'enable_exit': 0
}

# Get the first part of the local setting, required for the docutils parser
# that don't support the pattern ``xx_XX``.
RSTVIEW_PARSER_LANGUAGE_CODE = "en"

# The docutils writer to use, can be html4 (suitable for xhtml too) or html5,
# html5 writer is internal code
RSTVIEW_PARSER_WRITER = "html5"

# Disable unsafe ReSTructured directives, enable them at your own risk
RSTVIEW_PARSER_ENABLE_FILE_INSERTION = False
RSTVIEW_PARSER_ENABLE_RAW_INSERTION = False

# Available parser settings
# These are options only for docutils parser, see
# http://docutils.sourceforge.net/docs/user/config.html (The used writer is
# ``html4css1``)
RSTVIEW_PARSER_FILTER_SETTINGS = {
    'default':{
        'initial_header_level': 3,
        'file_insertion_enabled': RSTVIEW_PARSER_ENABLE_FILE_INSERTION,
        'raw_enabled': RSTVIEW_PARSER_ENABLE_RAW_INSERTION,
        'language_code': RSTVIEW_PARSER_LANGUAGE_CODE,
        'footnote_references': 'superscript',
        'doctitle_xform': False,
    },
}

# CSS class prefix for generated Pygments elements
RSTVIEW_PYGMENTS_CONTAINER_CLASSPREFIX = "pygments"
# Enable use of inline CSS styles in HTML generated by Pygments, this will fill
# your HTML with a lot a styles. Disabled by default
RSTVIEW_PYGMENTS_INLINESTYLES = False

# Template string used to format error from ``rst.viewreporter.SourceReporter``
RSTVIEW_ERROR_TEMPLATE = u"Line {lineno} : {message}"
