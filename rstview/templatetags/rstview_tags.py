# -*- coding: utf-8 -*-
"""

.. _templatetags-intro:

Template tags
=============

"""
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

from rstview.parser import RstExtendedRenderer

register = template.Library()


@register.simple_tag
def rst_render(source, *args, **kwargs):
    """
    Parse and render given string using a parser configuration.

    Examples:

        Basic usage: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING %}

        Using a specific config set: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING config='myconfig' %}

        Muting error and warning from parser: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING silent=True %}

        Everything joined: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING config='myconfig' silent=True %}

        Tag signature: ::

            {% rst_render SOURCE_STRING [config='default'] [silent=True] %}


    Args:
        source (string): reStructuredText markup to parse.

    Keyword Arguments:
        config (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
        silent (bool): Enable to override default *silent mode* behavior.
            Default value is the same as ``settings.RSTVIEW_PARSER_SILENT``.

    Returns:
        string: Rendered source from parser.
    """  # noqa: E501
    config_name = kwargs.get('config', 'default')
    silent = kwargs.get('silent', settings.RSTVIEW_PARSER_SILENT)
    parser = RstExtendedRenderer()

    # ``body_only`` is enforced to True else tag would return a dict of values
    # serialized to a string.
    return mark_safe(
        parser.parse(
            source,
            setting_key=config_name,
            body_only=True,
            silent=silent,
        )
    )
