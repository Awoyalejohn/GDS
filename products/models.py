from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

