# -*- coding: utf-8 -*-
"""
Template tags
=============

"""
from django import template
from django.utils.safestring import mark_safe

from rstview.parser import SourceParser

register = template.Library()


@register.simple_tag
def rst_render(source, *args, **kwargs):
    """
    Parse and render given string source using given parser option set.

    Examples:

        Basic usage: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING %}

        Using a specific config set: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING config='myconfig' %}

        Muting error and warning from parser: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING silent=False %}

        Everything joined: ::

            {% load rstview_tags %}

            {% rst_render SOURCE_STRING config='myconfig' silent=False %}

        Tag signature: ::

            {% rst_render SOURCE_STRING [config='default'] [silent=False] %}


    Args:
        source (string): reStructuredText markup to parse.

    Keyword Arguments:
        config (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
        silent (bool): If ``True``, parser won't include errors and warning
            in rendered source. Default is ``False``.

    Returns:
        string: Rendered source from parser.
    """  # noqa: E501
    config_name = kwargs.get('config', 'default')
    silent = kwargs.get('silent', False)

    # ``body_only`` is enforced to True else tag would return a dict of values
    # serialized to a string.
    return mark_safe(
        SourceParser(
            source,
            setting_key=config_name,
            body_only=True,
            silent=silent,
        )
    )
