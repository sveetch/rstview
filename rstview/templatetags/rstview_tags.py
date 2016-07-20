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
    Parse and render given string source using given config set.

    **Usage:** ::

        {% load rstview_tags %}

        {% rst_render SOURCE_STRING [config='default'] [body_only=True] [silent=False] %}


    Args:
        source (string): reStructuredText markup to parse.

    Keyword Arguments:
        config (string): Name of an option set from
            ``settings.RSTVIEW_PARSER_FILTER_SETTINGS``.
        body_only (bool): If ``True``, parser won't include errors and warning
            in rendered source. Default is ``False``.
        silent (bool): If ``True``, parser will only return the rendered
            content, this is the default behavior.

    Returns:
        string: Rendered source from parser.
    """  # noqa: E501
    config_name = kwargs.get('config', 'default')
    body_only = kwargs.get('body_only', True)
    silent = kwargs.get('silent', False)

    return mark_safe(
        SourceParser(
            source,
            setting_key=config_name,
            body_only=body_only,
            silent=silent,
        )
    )
