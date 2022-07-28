from django.urls import path
from products.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
]