from django.urls import path
from .views import WishListView

urlpatterns = [
    path('', WishListView.as_view(), name='wish_list'),
]