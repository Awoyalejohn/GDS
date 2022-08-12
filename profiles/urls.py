from django.urls import path
from profiles.views import Profile, OrderHistory, ProfileDownloads

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
    path('order_history/<order_number>', OrderHistory.as_view(), name='order_history'),
    path('order_history/<order_number>/downloads', ProfileDownloads.as_view(), name='profile_downloads'),
]