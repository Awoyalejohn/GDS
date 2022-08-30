from django.urls import path
from .views import UpdateReview, DeleteReview

urlpatterns = [
    path(
        "edit_review/<review_id>",
        UpdateReview.as_view(),
        name="edit_review"
    ),
    path(
        "delete_review/<review_id>",
        DeleteReview.as_view(),
        name="delete_review"
        ),
]
