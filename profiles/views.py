from django.shortcuts import render
from django.views.generic import TemplateView

class Profile(TemplateView):
    """ Display the user's Profile """
    template_name = "profiles/profile.html"