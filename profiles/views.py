from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order

class Profile(LoginRequiredMixin, View):
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
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')



class OrderHistory(LoginRequiredMixin, TemplateView):
     template_name = 'checkout/checkout_success.html'
     def get_context_data(self, order_number, **kwargs):
        context = super(OrderHistory, self).get_context_data(**kwargs)
        order = get_object_or_404(Order, order_number=order_number)

        messages.info(self.request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
        ))
        context['order'] = order
        context['from_profile'] = True
        return context


class ProfileDownloads(TemplateView):
    """ A view display orders for users to download """
    template_name = 'profiles/profile_downloads.html'

    def get_context_data(self, order_number, **kwargs):
        context = super(ProfileDownloads, self).get_context_data(**kwargs)
        order = get_object_or_404(Order, order_number=order_number)
        context['order'] = order
        return context


