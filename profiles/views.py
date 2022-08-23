from django.shortcuts import get_object_or_404, render, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import UserProfileForm, UserForm, ProfileInfoForm

from checkout.models import Order

class ProfileInfo(LoginRequiredMixin, View):
    """ A view to display form info from the user model """
    def get(self, request):
        # from django update user profile tutorial https://dev.to/earthcomfy/django-update-user-profile-33ho
        profile = get_object_or_404(UserProfile, user=request.user)
        user_form = UserForm(instance=request.user)
        profile_info_form = ProfileInfoForm(instance=profile)
        template = 'profiles/profile_info.html'
        context = {
            'profile': profile,
            'user_form': user_form,
            'profile_info_form': profile_info_form
        }
        return render(request, template, context)

    def post(self, request):
        # from django update user profile tutorial https://dev.to/earthcomfy/django-update-user-profile-33ho
        profile = get_object_or_404(UserProfile, user=request.user)
        user_form = UserForm(self.request.POST, instance=request.user)
        profile_info_form = ProfileInfoForm(self.request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_info_form.is_valid():
            user_form.save()
            profile_info_form.save()
            messages.success(request, 'Your Profile has been updated successfully')
            return HttpResponseRedirect(reverse('profile_info'))


class ProfileBillingDetails(LoginRequiredMixin, View):
    """ Display the user's Profile """
    template_name = "profiles/profile.html"
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=profile)
        template = 'profiles/profile_billing_details.html'
        context = {
            'profile':profile,
            'form': form,
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
     template_name = 'profiles/profile_order_history.html'
     def get_context_data(self, **kwargs):
        context = super(OrderHistory, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        orders = profile.orders.all()
        context['orders'] = orders
        return context


class OrderHistoryDetail(LoginRequiredMixin, TemplateView):
     template_name = 'checkout/checkout_success.html'
     def get_context_data(self, order_number, **kwargs):
        context = super(OrderHistoryDetail, self).get_context_data(**kwargs)
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


