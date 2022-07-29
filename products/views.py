from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
from products.models import Product

# Create your views here.
class ProductListView(View):
    """ A view to list all products """
    def get(self, request):
        products = Product.objects.all()
        context = {'product_list': products}
        return render(request, 'products/product_list.html', context)




class ProductDetailView(DetailView):
    """ 
    A view to display and individual item's product page
    """
    model = Product
