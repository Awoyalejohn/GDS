import imp
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    """ A view to return the index page """
    
    template_name = "home/index.html"
