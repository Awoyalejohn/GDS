from django.db import models
from profiles.models import UserProfile
from quotes.choices import TYPE_CHOICES, SIZE_CHOICES

import uuid

# Create your models here.
class QuoteRequest(models.Model):
    name = models.CharField(max_length=250)
    user =  models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    description = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    quote_request_number = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class QuoteOrder(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    quote_request_name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    size = models.CharField(max_length=250)
    description = models.TextField()
    subtotal = models.CharField(max_length=250)
    discount = models.CharField(max_length=250)
    total = models.CharField(max_length=250)
    submitted = models.DateTimeField(auto_now_add=True)
    quote_order_number = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.quote_request_name


class QuoteFufillment(models.Model):
    quote_order = models.OneToOneField(QuoteOrder, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.quote_order
