from django.urls import path
from products.views import (
    ProductListView,
    ProductDetailView,
    AddProductView,
    EditProductView,
    DeleteProductView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('add/', AddProductView.as_view(), name='add_product'),
    path('edit/<slug:slug>/', EditProductView.as_view(), name='edit_product'),
    path('delete/<slug:slug>/', DeleteProductView.as_view(), name='delete_product'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]