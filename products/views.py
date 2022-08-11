from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from products.models import Product, Category
from .forms import ProductForm

# Create your views here.
class ProductListView(View):
    """ A view to list all products """
    def get(self, request):
        products = Product.objects.all()
        query = None
        categories = None
        sort = None
        direction = None

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__slug__in=categories)
            categories = Category.objects.filter(slug__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))
            
            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
            products = products.filter(queries)
        
        current_sorting = f'{sort}_{direction}'

        context = {
            'product_list': products,
            'search_term': query,
            'current_categories': categories,
            'current_sorting': current_sorting
            }
        return render(request, 'products/product_list.html', context)




class ProductDetailView(DetailView):
    """ 
    A view to display and individual item's product page
    """
    model = Product



class AddProductView(CreateView):
    """ Add a product to the store """
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = '/products/'


