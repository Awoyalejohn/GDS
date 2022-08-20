from django.urls import path
from quotes.views import (
    QuoteRequestView, QuoteCheckoutView, QuoteCheckoutSuccess,
    QuoteHistoryView, QuoteHistoryDetail, QuoteOrderList,
    QuoteOrderFufillCreate, QuoteOrderFufillUpdate
    )

urlpatterns = [
    path('', QuoteRequestView.as_view(), name='quote_request'),
    path('quote_orders', QuoteOrderList.as_view(), name='quote_orders'),
    path('quote_orders/fufill/<quote_order_number>', QuoteOrderFufillCreate.as_view(), name='quote_orders_fufill'),
    path('quote_orders/fufill/update/<quote_order_number>', QuoteOrderFufillUpdate.as_view(), name='quote_fufill_update'),
    path('quote_history/', QuoteHistoryView.as_view(), name='quote_history'),
    path('quote_history/<quote_order_number>', QuoteHistoryDetail.as_view(), name='quote_history_detail'),
    path('quote_checkout/', QuoteCheckoutView.as_view(), name='quote_checkout'),
    path('quote_checkout_success/<quote_order_number>', QuoteCheckoutSuccess.as_view(), name='quote_checkout_success'),
]