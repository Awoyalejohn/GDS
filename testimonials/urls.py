from django.urls import path
from .views import TestimonialListView, AddTestimonialView, EditTestimonialView

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonials'),
    path('add_testimonial/', AddTestimonialView.as_view(), name='add_testimonial'),
    path('edit_testimonial/<int:id>', EditTestimonialView.as_view(), name='edit_testimonial'),
]