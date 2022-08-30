from django.urls import path
from .views import (
    TestimonialListView,
    AddTestimonialView,
    EditTestimonialView,
    DeleteTestimonialView,
    ApproveTestimonialsView,
)

urlpatterns = [
    path("", TestimonialListView.as_view(), name="testimonials"),
    path(
        "add_testimonial/",
        AddTestimonialView.as_view(),
        name="add_testimonial"
        ),
    path(
        "edit_testimonial/<int:id>",
        EditTestimonialView.as_view(),
        name="edit_testimonial",
    ),
    path(
        "delete_testimonial/<int:id>",
        DeleteTestimonialView.as_view(),
        name="delete_testimonial",
    ),
    path(
        "approve_testimonials",
        ApproveTestimonialsView.as_view(),
        name="approve_testimonials",
    ),
]
