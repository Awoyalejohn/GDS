from django.db import models

from products.models import Product
from profiles.models import UserProfile

class Review(models.Model):
    rating = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_review')
    body = models.TextField()
    submitted =  models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
