from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
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
        selected_type = None
        type = request.POST['type']
        if type == 'IC' or type == 'ST':
            type_cost = 9.99
            if type == 'IC':
                selected_type = 'Icon'
            else:
                selected_type = 'Sticker'
        elif type == 'LG' or type == 'BN':
            type_cost = 19.99
            if type == 'LG':
                selected_type = 'Logo'
            else:
                selected_type = 'Banner'
        elif type == 'PS' or type == 'WP':
            type_cost = 39.99
            if type == 'PS':
                selected_type = 'Poster'
            else:
                selected_type = 'Wallpaper'            
        else:
            messages.error(request, 'Something went wrong wth your request')
            return redirect(reverse('quote_request'))
        print(type_cost)

        size_cost = None
        selected_size = None

        size = request.POST['size']
        if size == 'S':
            size_cost = 9.99
            selected_size = 'Small'
        elif size == 'M':
            size_cost = 19.99
            selected_size = 'Medium'
        elif size == 'L':
            size_cost = 29.99
            selected_size = 'Large'
        else:
            messages.error(request, 'Something went wrong wth your request')
            return redirect(reverse('quote_request'))

        print(size_cost)

        subtotal = round(type_cost + size_cost, 2)
        print(subtotal)

        if subtotal > settings.DISCOUNT_THRESHOLD:
            discount = ceil(subtotal * settings.DISCOUNT_PERCENTAGE / 100)
        
        else:
            discount = 0
        
        total = (round(subtotal - discount, 2)) 
        print(discount)
        print(total)

        # stripe_total = round(total * 100)

     

        # intent = stripe.PaymentIntent.create(
        #     amount=stripe_total,
        #     currency=settings.STRIPE_CURRENCY,
        #     payment_method_types=['card'],
        # )

        # print(intent)
        quote_description = request.POST['description']


        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['quote_description'] = quote_description
            request.session['quote_subtotal'] = subtotal
            request.session['quote_discount'] = discount
            request.session['quote_total'] = total
            request.session['selected_type'] = selected_type
            request.session['selected_size'] = selected_size
            messages.success(request, 'Thank you for your request')
            return HttpResponseRedirect(reverse('quote_checkout'))


class QuoteCheckoutView(View):
     """ A view to checkout quote after getting the data from the QuoteRequestView """
     def get(self, request):
        template = 'quotes/quote_checkout.html'
        quote_description = request.session['quote_description']
        quote_subtotal = request.session['quote_subtotal']
        quote_discount = request.session['quote_discount']
        quote_total = request.session['quote_total']
        selected_type = request.session['selected_type']
        selected_size = request.session['selected_size']
        context = {
            'quote_description': quote_description,
            'quote_subtotal': quote_subtotal,
            'quote_discount': quote_discount,
            'quote_total': quote_total,
            'selected_type': selected_type,
            'selected_size': selected_size,
        }

        return render(request, template, context)
