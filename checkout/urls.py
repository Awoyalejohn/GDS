from django.urls import path
from checkout.views import Checkout, CheckoutSuccess, cache_checkout_data
from .webhooks import webhook

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('checkout_success/<order_number>', CheckoutSuccess.as_view(), name='checkout_success'),
    path('cache_checkout_data/', cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]