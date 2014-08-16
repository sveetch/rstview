# -*- coding: utf-8 -*-
"""
Parser template tags 
"""
from django import template
from django.utils.safestring import mark_safe

from rstview.parser import SourceParser

register = template.Library()

def source_render(source, setting_key="default"):
    """
    Return the parser result from the given string source and settings
    """
    return mark_safe( SourceParser(source, setting_key=setting_key) )
source_render.is_safe = True
register.filter(source_render)
