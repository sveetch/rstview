# -*- coding: utf-8 -*-
"""
ReStructuredText views
"""
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.views.generic import TemplateView

from rstview import parser

class RSTFileView(TemplateView):
    """
    View to display a ReST file
    
    Open the file, parse it and put his source and render into the context
    """
    template_name = "rstview/fileview.html"
    doc_title = None
    doc_file_path = None
    
    def get_context_data(self, **kwargs):
        context = super(RSTFileView, self).get_context_data(**kwargs)
        
        f = open(self.doc_file_path,'r')
        source = f.read()
        f.close()
        
        context.update({
            'doc_title': self.doc_title,
            'doc_source': source,
        })
        return context
