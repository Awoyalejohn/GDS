from django.urls import path
from checkout.views import Checkout

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
]