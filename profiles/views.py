from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import UserProfile

class Profile(TemplateView):
    """ Display the user's Profile """
    template_name = "profiles/profile.html"
    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['profile'] = get_object_or_404(UserProfile, user=self.request.user)
        return context

        