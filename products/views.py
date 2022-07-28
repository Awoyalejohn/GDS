from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from products.models import Product

# Create your views here.
class ProductListView(ListView):
    """ A view to list all products """
    model = Product

class ProductDetailView(DetailView):
    """ A view to display and individual item's product page """
    model = Product
