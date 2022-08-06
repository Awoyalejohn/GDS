from django.urls import path
from profiles.views import Profile

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
]