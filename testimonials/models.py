from django.db import models
from profiles.models import UserProfile

# Create your models here.
class Testimonial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_testmonial')
    body = models.TextField()
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.user.user.username