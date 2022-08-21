from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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


class AddTestimonialView(CreateView):
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


class EditTestimonialView(UpdateView):
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


class DeleteTestimonialView(SuccessMessageMixin, DeleteView):
    """ Deletes a testimonial """
    model = Testimonial
    template_name = 'testimonials/delete_testimonial.html'
    success_url = reverse_lazy('testimonials')
    success_message = 'Successfully deleted testimonial!'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Testimonial, id=id)


class ApproveTestimonialsView(View):
    """ A view for approving user testimonials  """
    def get(self, request):
        template = 'testimonials/approve_testimonials.html'
        context = {}

        return render(request, template, context)




