# -*- coding: utf-8 -*-
"""
Parser template tags
"""
from django import template
from django.utils.safestring import mark_safe

from rstview.parser import SourceParser

register = template.Library()


@register.simple_tag
def rst_render(source, *args, **kwargs):
    """
    Return the parser result from the given string source and settings

    {% rst_render SOURCE_STRING [config='default'] [body_only=True] [silent=False] %}
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
