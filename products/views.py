from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic import View
from django.views.generic.detail import DetailView
from products.models import Product, Category

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
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)



        if 'category' in request.GET:
            categories = request.GET['category']
            products = products.filter(category__name__icontains=categories)
            categories = Category.objects.filter(name__icontains=categories)

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
