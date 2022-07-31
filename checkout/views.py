from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import View
from .forms import OrderForm

# Create your views here.
class Checkout(View):
    """ A view to add items to the cart page """
    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
        }

        return render(request, template, context)