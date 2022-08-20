from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from products.models import Product, Category
from .forms import ProductForm
from reviews.forms import ReviewForm
from django.db.models import Avg

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


class ProductDetailView(View):
    """ 
    A view to display and individual item's product page
    And to create and display customer product reviews
    """
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        reviews = product.product_review.all()
        avg_reviews = product.product_review.all().aggregate(Avg('rating'))
        print(avg_reviews)
        form = ReviewForm()

        # Display recently viewed products code from sessions tutourial on youtube
        # https://www.youtube.com/watch?v=N-R5mT-nIDk&t=989s
        recently_viewed_products = None

        if 'recently_viewed' in request.session:
            if slug in request.session['recently_viewed']:
                request.session['recently_viewed'].remove(slug)
            
            products = Product.objects.filter(slug__in=request.session['recently_viewed'])
            recently_viewed_products = sorted(
                products, key=lambda x: request.session['recently_viewed'].index(x.slug)
            )

            request.session['recently_viewed'].insert(0, slug)
            if len(request.session['recently_viewed']) > 5:
                request.session['recently_viewed'].pop()
        else:
            request.session['recently_viewed'] = [slug]
        
        request.session.modified = True

        related_products = Product.objects.filter(category=product.category).exclude(slug=slug)[:5]
        print(request.session['recently_viewed'])


        template = 'products/product_detail.html'
        context = {
            'product': product,
            'reviews': reviews,
            'form': form,
            'avg_reviews': avg_reviews,
            'recently_viewed_products':recently_viewed_products,
            'related_products': related_products,
        }
        return render(request, template, context)
    
    def post(self, request, slug):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review was successful')
            return HttpResponseRedirect(self.request.path_info)



class SuperUserCheck(UserPassesTestMixin, View):
    """ 
    A CBV mixin to prevent access from users that are not superusers
    """
    def test_func(self):
        return self.request.user.is_superuser


class AddProductView(SuperUserCheck, CreateView):
    """ Add a product to the store """
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_message = 'Successfully added product!'
    error_message = 'Failed to add product. Please ensure the form is valid.'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class EditProductView(SuperUserCheck, UpdateView):
    """ Edits a product in the store """
    model = Product
    form_class = ProductForm
    template_name = 'products/edit_product.html'
    success_message = 'Successfully Updated product!'
    error_message = 'Failed to update product. Please ensure the form is valid.'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(EditProductView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.object.slug)

        messages.info(self.request, f'You are editing {product.name}')
        context['product'] = product
        return context


class DeleteProductView(SuperUserCheck, SuccessMessageMixin, DeleteView):
    """ Deletes a product in the store """
    model = Product
    template_name = 'products/delete_product.html'
    success_url = reverse_lazy('products')
    success_message = 'Successfully deleted product!'

