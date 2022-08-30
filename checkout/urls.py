from django.urls import path
from checkout.views import (
    Checkout,
    CheckoutSuccess,
    cache_checkout_data,
    CheckoutDownloads,
)
from .webhooks import webhook

urlpatterns = [
    path("", Checkout.as_view(), name="checkout"),
    path(
        "checkout_success/<order_number>",
        CheckoutSuccess.as_view(),
        name="checkout_success",
    ),
    path(
        "checkout_success/<order_number>/downloads",
        CheckoutDownloads.as_view(),
        name="checkout_downloads",
    ),
    path(
        "cache_checkout_data/",
        cache_checkout_data,
        name="cache_checkout_data"
    ),
    path("wh/", webhook, name="webhook"),
]
