from django.urls import path
from checkout.views import Checkout, CheckoutSuccess

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('checkout_success/<order_number>', CheckoutSuccess.as_view(), name='checkout_success'),
]