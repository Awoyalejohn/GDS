from django.urls import path
from products.views import ProductListView, ProductDetailView, AddProductView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('add/', AddProductView.as_view(), name='add_product'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]