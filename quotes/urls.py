from django.urls import path
from quotes.views import QuoteRequestView, QuoteCheckoutView

urlpatterns = [
    path('', QuoteRequestView.as_view(), name='quote_request'),
    path('quote_checkout/', QuoteCheckoutView.as_view(), name='quote_checkout'),
]