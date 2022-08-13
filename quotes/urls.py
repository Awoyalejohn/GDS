from django.urls import path
from quotes.views import QuoteRequestView

urlpatterns = [
    path('', QuoteRequestView.as_view(), name='quote_request'),
]