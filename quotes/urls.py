from django.urls import path
from quotes.views import QuoteRequestView, QuoteCheckoutView, QuoteCheckoutSuccess, QuoteHistoryView, QuoteHistoryDetail
urlpatterns = [
    path('', QuoteRequestView.as_view(), name='quote_request'),
    path('quote_history/', QuoteHistoryView.as_view(), name='quote_history'),
    path('quote_history/<quote_order>', QuoteHistoryDetail.as_view(), name='quote_history_detail'),
    path('quote_checkout/', QuoteCheckoutView.as_view(), name='quote_checkout'),
    path('quote_checkout_success/<quote_order_number>', QuoteCheckoutSuccess.as_view(), name='quote_checkout_success'),
]