from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Testimonial
from profiles.models import UserProfile
from .forms import TestimonialForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View


# Create your views here.
class TestimonialListView(ListView):
    """ Displays a list of all approved user testimonials """
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'


class AddTestimonialView(LoginRequiredMixin, CreateView):
    """ creates and adds a user testimonial to be approved for the testimonila page """
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonials/add_testimonial.html'
    success_message = 'Successfully added testimonial'
    error_message = 'Failed to add testimonial. Please ensure the form is valid.'

    def get_success_url(self):
        return reverse_lazy('testimonials')

    def form_valid(self, form):
        form.instance.user = UserProfile.objects.get(user=self.request.user)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class EditTestimonialView(UserPassesTestMixin, UpdateView):
    """ A view for users to edit Testimonials """
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonials/edit_testimonial.html'
    success_message = 'Successfully updated testimonial'
    error_message = 'Failed to update testimonial. Please ensure the form is valid.'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Testimonial, id=id)

    def get_success_url(self):
        return reverse_lazy('testimonials')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    # restric access mixin from https://stackoverflow.com/questions/58217055/how-can-i-restrict-access-to-a-view-to-only-super-users-in-django
    def test_func(self):
        id = self.kwargs.get("id")
        testimonial = get_object_or_404(Testimonial, id=id)
        return self.request.user.is_superuser or self.request.user == testimonial.user.user


class DeleteTestimonialView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """ Deletes a testimonial """
    model = Testimonial
    template_name = 'testimonials/delete_testimonial.html'
    success_url = reverse_lazy('testimonials')
    success_message = 'Successfully deleted testimonial!'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Testimonial, id=id)

    # restric access mixin from https://stackoverflow.com/questions/58217055/how-can-i-restrict-access-to-a-view-to-only-super-users-in-django
    def test_func(self):
        id = self.kwargs.get("id")
        testimonial = get_object_or_404(Testimonial, id=id)
        return self.request.user.is_superuser or self.request.user == testimonial.user.user
        

class SuperUserCheck(UserPassesTestMixin, View):
    """ 
    A CBV mixin to prevent access from users that are not superusers
    From https://stackoverflow.com/questions/67351312/django-check-if-superuser-in-class-based-view

    """
    def test_func(self):
        return self.request.user.is_superuser

class ApproveTestimonialsView(SuperUserCheck, View):
    """ A view for approving user testimonials  """
    def get(self, request):
        # From Approval with checkboxes tutorial on You Tube
        # https://www.youtube.com/watch?v=FzV_Py68Y_I

        testimonials = Testimonial.objects.all()
        template = 'testimonials/approve_testimonials.html'
        context = {'testimonials': testimonials}

        return render(request, template, context)
    
    def post(self, request):
        testimonials = Testimonial.objects.all()
        checkboxes = request.POST.getlist('checkboxes')

        # Uncheck all events
        testimonials.update(approved=False)

        # Update the database
        for checkbox in checkboxes:
            Testimonial.objects.filter(pk=int(checkbox)).update(approved=True)

        messages.success(request, "Successfully updated Testimonial approvals")
        return HttpResponseRedirect(reverse('testimonials'))





