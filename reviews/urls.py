from django.urls import path
from .views import UpdateReview

urlpatterns = [
    path('edit_review/<review_id>', UpdateReview.as_view(), name='edit_review'),

]