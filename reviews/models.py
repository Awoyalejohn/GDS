from django.db import models

from products.models import Product
from profiles.models import UserProfile

class Review(models.Model):
    rating = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    submitted =  models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
