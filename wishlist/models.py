from django.db import models
from profiles.models import UserProfile
from products.models import Product 

# Create your models here.
class WishList(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wish_list')

    def __str__(self):
        return f"{self.user_profile}'s Wish List"


class WishListItem(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wish_list_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_list_item')

    class Meta:
        unique_together = ('wish_list', 'product')