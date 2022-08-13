from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from .forms import QuoteRequestForm
from math import ceil

from django.http import JsonResponse

import stripe
# Create your views here.
class QuoteRequestView(View):
    """ A view to request and purchase a specific graphic design """
    def get(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = stripe_secret_key
        form = QuoteRequestForm()

        template = 'quotes/quote_request.html'
        context = {
            'form': form,
            'stripe_public_key': stripe_public_key,
            'stripe_secret_key': stripe_secret_key,

        }


        return render(request, template, context)
    
    def post(self, request):

        print(request.POST)
        type_cost = None
        size_cost = None
        type = request.POST['type']
        if type == 'IC' or type == 'ST':
            type_cost = 9.99
        elif type == 'LG' or type == 'BN':
            type_cost = 19.99
        elif type == 'PS' or type == 'WP':
            type_cost = 39.99
        else:
            messages.error(request, 'Something went wrong wth your request')
            return redirect(reverse('quote_request'))
        print(type_cost)

        size = request.POST['size']
        if size == 'S':
            size_cost = 9.99
        elif size == 'M':
            size_cost = 19.99
        elif size == 'L':
            size_cost = 29.99
        else:
            messages.error(request, 'Something went wrong wth your request')
            return redirect(reverse('quote_request'))

        print(size_cost)

        subtotal = round(type_cost + size_cost, 2)
        print(subtotal)

        if subtotal > settings.DISCOUNT_THRESHOLD:
            discount = ceil(subtotal * settings.DISCOUNT_PERCENTAGE / 100)
            discount_delta = 0
        
        else:
            discount = 0
            discount_delta = settings.DISCOUNT_THRESHOLD - subtotal
        
        total = (round(subtotal - discount, 2)) 
        print(discount)
        print(total)

        stripe_total = round(total * 100)

     

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            payment_method_types=['card'],
        )

        print(intent)


        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your request')
            return JsonResponse({'clientSecret': intent.client_secret}), redirect(reverse('quote_request'))
