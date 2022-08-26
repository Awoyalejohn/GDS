from django.urls import path
from profiles.views import ProfileBillingDetails, OrderHistory, OrderHistoryDetail, ProfileDownloads, ProfileInfo, ProfileReviews, ProfileTestimonials

urlpatterns = [
    path('', ProfileInfo.as_view(), name='profile_info'),
    path('profile_billing_details/', ProfileBillingDetails.as_view(), name='profile_billing_details'),
    path('order_history/', OrderHistory.as_view(), name='order_history'),
    path('order_history_detail/<order_number>', OrderHistoryDetail.as_view(), name='order_history_detail'),
    path('order_history_detail/<order_number>/downloads', ProfileDownloads.as_view(), name='profile_downloads'),
    path('reviews/', ProfileReviews.as_view(), name='profile_reviews'),
    path('testimonials/', ProfileTestimonials.as_view(), name='profile_testimonials'),
]