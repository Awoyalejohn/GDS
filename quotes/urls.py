from django.urls import path
from quotes.views import QuoteRequestView, QuoteCheckout

urlpatterns = [
    path('', QuoteRequestView.as_view(), name='quote_request'),
    path('quote_checkout/', QuoteCheckout.as_view(), name='quote_checkout'),
]