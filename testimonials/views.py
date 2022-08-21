from django.shortcuts import render
from .models import Testimonial
from django.views.generic import ListView


# Create your views here.
class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'