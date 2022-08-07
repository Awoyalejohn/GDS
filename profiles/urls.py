from django.urls import path
from profiles.views import Profile, OrderHistory

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
    path('order_history/<order_number>', OrderHistory.as_view(), name='order_history'),
]