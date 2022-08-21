from django.urls import path
from .views import TestimonialListView, AddTestimonialView

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonials'),
    path('add_testimonial', AddTestimonialView.as_view(), name='add_testimonial'),
]