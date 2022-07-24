from django.shortcuts import render
from django.views.generic.list import ListView
from products.models import Product

# Create your views here.
class ProductListView(ListView):
    """ A view to list all products """
    model = Product
