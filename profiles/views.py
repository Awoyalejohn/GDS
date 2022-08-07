from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import UserProfileForm

class Profile(View):
    """ Display the user's Profile """
    template_name = "profiles/profile.html"
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=profile)
        orders = profile.orders.all()
        template = 'profiles/profile.html'
        context = {
            'profile':profile,
            'form': form,
            'orders': orders
        }
        return render(request, template, context)

    def post (self, request):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(self.request.path_info)

