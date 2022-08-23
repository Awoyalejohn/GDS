from django.urls import path
from .views import WishListView, AddToWishList, RemoveFromWishList

urlpatterns = [
    path('', WishListView.as_view(), name='wish_list'),
    path('add/<slug:slug>/', AddToWishList.as_view(), name='add_to_wish_list'),
    path('remove/<slug:slug>/', RemoveFromWishList.as_view(), name='remove_from_wish_list'),
]