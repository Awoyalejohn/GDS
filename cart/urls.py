from django.urls import path
from cart.views import DisplayCartView, AddToCart

urlpatterns = [
    path('', DisplayCartView.as_view(), name='display_cart'),
    path('add/<slug:slug>/', AddToCart.as_view(), name='add_to_cart'),
]