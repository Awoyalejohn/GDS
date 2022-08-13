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
    quote_order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name
