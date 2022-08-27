from django.shortcuts import get_object_or_404, render, redirect, reverse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from cart.contexts import cart_contents

import stripe
from django.http import JsonResponse
import json







@require_POST
def cache_checkout_data(request):
    try:
        req_json = json.loads(request.body)
        pid = req_json['client_secret'].split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': req_json['save_info'],
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)



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


        # Checks if the user is authenticated, if it is true it gets the profile
        # and prefills all its fields with the relaevant data for the order form
        if self.request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=self.request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for slug, item_data in cart.items():
                try:
                    product = Product.objects.get(slug=slug)
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

        if self.request.user.is_authenticated:
            profile = UserProfile.objects.get(user=self.request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            order.save()

            # Save the user's info
            if save_info:
                profile_data = {
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
   
        messages.success(request, f"Order successfuly processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.")
        
        if 'cart' in request.session:
            del request.session['cart']
        
        template = 'checkout/checkout_success.html'
        context = {'order':order,}
        return render(request, template, context)




class CheckoutDownloads(TemplateView):
    """ A view display orders for users to download """
    template_name = 'checkout/checkout_downloads.html'

    def get_context_data(self, order_number, **kwargs):
        context = super(CheckoutDownloads, self).get_context_data(**kwargs)
        order = get_object_or_404(Order, order_number=order_number)
        context['order'] = order
        return context
        