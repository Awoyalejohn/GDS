from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import View
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.contexts import cart_contents

import stripe

# Create your views here.
class Checkout(View):
    """ A view to allow purchasing of the items from the checkout page """
    def get(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(intent)


        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


    def post(self, request):
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for slug, item_data in cart.items():
                print(cart.items())
                try:
                    product = Product.objects.get(slug=slug)
                    print(product)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('display_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')


class CheckoutSuccess(View):
    """
    A view to handle successful checkouts
    """
    def get(self, request, order_number):
        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)
        messages.success(request, f"Order successfuly processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.")
        
        if 'cart' in request.session:
            del request.session['cart']
        
        template = 'checkout/checkout_success.html'
        context = {'order':order,}
        return render(request, template, context)
        