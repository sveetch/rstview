# -*- coding: utf-8 -*-
import os

import pytest

from rstview import reporter

from django.utils.translation import ugettext_lazy as _


def test_validate_basic_content(settings):
    """Try to validate a basic valid input"""
    source = """Lorem **ipsum** salace"""

    errors = reporter.SourceReporter(source)

    assert errors == []


def test_validate_invalid_syntax(settings):
    """Try to validate a basic invalid input"""
    source = """Lorem **ipsum salace"""

    errors = reporter.SourceReporter(source)

    assert errors == [
        (2, 'Inline strong start-string without end-string.', (), {'line': 1}),
    ]

    assert map(reporter.format_parsing_errors, errors) == [
        u'Line 1 : Inline strong start-string without end-string.',
    ]


def test_validate_invalid_syntax_i18n(settings):
    """Try to validate a basic invalid input with ugettext fonction used on
       error template"""
    settings.RSTVIEW_ERROR_TEMPLATE = _(u"Line é {lineno} : {message}")

    source = """Lorem **ipsum salace"""

    errors = reporter.SourceReporter(source)

    assert errors == [
        (2, 'Inline strong start-string without end-string.', (), {'line': 1}),
    ]

    assert map(reporter.format_parsing_errors, errors) == [
        u'Line é 1 : Inline strong start-string without end-string.',
    ]


#def test_validate_invalid_multiple(settings):
    #"""
    #Multiple error on the same document
    #"""
    #input_filepath = os.path.join(settings.TESTS_FIXTURES_DIR, "invalid/input.rst")
    #with open(input_filepath, 'r') as fp:
        #source = fp.read()

    #errors = reporter.SourceReporter(source)

    #assert errors == []

    #assert 1 == 42