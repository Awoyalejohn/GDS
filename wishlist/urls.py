from django.urls import path
from .views import WishListView, AddToWishList

urlpatterns = [
    path('', WishListView.as_view(), name='wish_list'),
    path('add/<slug:slug>/', AddToWishList.as_view(), name='add_to_wish_list'),
]