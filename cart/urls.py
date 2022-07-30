from django.urls import path
from cart.views import DisplayCartView

urlpatterns = [
    path('', DisplayCartView.as_view(), name='display_cart'),
]