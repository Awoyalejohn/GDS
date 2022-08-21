from django.urls import path
from profiles.views import Profile, OrderHistory, OrderHistoryDetail, ProfileDownloads, ProfileInfo

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
    path('profile_info/', ProfileInfo.as_view(), name='profile_info'),
    path('order_history/', OrderHistory.as_view(), name='order_history'),
    path('order_history_detail/<order_number>', OrderHistoryDetail.as_view(), name='order_history_detail'),
    path('order_history_detail/<order_number>/downloads', ProfileDownloads.as_view(), name='profile_downloads'),
]