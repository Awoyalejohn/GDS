from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from profiles.models import UserProfile
from .models import QuoteOrder
from .forms import QuoteRequestForm, QuoteOrderForm
from math import ceil
import uuid


from django.http import JsonResponse

import stripe
# Create your views here.
class QuoteRequestView(LoginRequiredMixin, View):
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

        quote_item_name = request.POST['name']
        quote_description = request.POST['description']

        form = QuoteRequestForm(request.POST)
        form.instance.user = UserProfile.objects.get(user=self.request.user)
        uuid_number = str(uuid.uuid4())
        print(uuid_number)
        form.instance.quote_request_number = uuid_number  
        if form.is_valid():
            form.save()
            request.session['quote_item_name'] = quote_item_name
            request.session['quote_description'] = quote_description
            request.session['quote_subtotal'] = subtotal
            request.session['quote_discount'] = discount
            request.session['quote_total'] = total
            request.session['selected_type'] = selected_type
            request.session['selected_size'] = selected_size
            request.session['quote_request_number'] = uuid_number
            messages.success(request, 'Thank you for your request')
            return HttpResponseRedirect(reverse('quote_checkout'))


class QuoteCheckoutView(View):
     """ A view to checkout quote after getting the data from the QuoteRequestView """
     def get(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        form = QuoteOrderForm()
        quote_item_name = request.session['quote_item_name']
        quote_description = request.session['quote_description']
        quote_subtotal = request.session['quote_subtotal']
        quote_discount = request.session['quote_discount']
        quote_total = request.session['quote_total']
        selected_type = request.session['selected_type']
        selected_size = request.session['selected_size']
        quote_order_number = request.session['quote_request_number']

        stripe_total = round(quote_total * 100)
        stripe.api_key = stripe_secret_key
        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(payment_intent)

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set in your environment?')

        template = 'quotes/quote_checkout.html'

        context = {
            'form': form,
            'quote_item_name': quote_item_name,
            'quote_description': quote_description,
            'quote_subtotal': quote_subtotal,
            'quote_discount': quote_discount,
            'quote_total': quote_total,
            'selected_type': selected_type,
            'selected_size': selected_size,
            'quote_order_number': quote_order_number,
            'stripe_public_key': stripe_public_key,
            'client_secret': payment_intent.client_secret,
        }

        return render(request, template, context)

     def post(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        quote_order_number = request.session['quote_request_number']

        form = QuoteOrderForm(request.POST)
        form.instance.user = UserProfile.objects.get(user=self.request.user)
        form.instance.name = request.POST['name']
        form.instance.email = request.POST['email']
        form.instance.quote_request_name = request.session['quote_item_name']
        form.instance.type = request.session['selected_type']
        form.instance.size = request.session['selected_size']
        form.instance.description = request.session['quote_description']
        form.instance.subtotal = request.session['quote_subtotal']
        form.instance.discount = request.session['quote_discount']
        form.instance.total = request.session['quote_total']
        form.instance.quote_order_number = request.session['quote_request_number']

        # form = QuoteOrderForm(form_data)

        if form.is_valid():
            form.save()
            return redirect(reverse('quote_checkout_success', args=[quote_order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
            Please double check your information.')


class QuoteCheckoutSuccess(View):
    """ A view to handle successful quote request checkouts """
    def get(self, request, quote_order_number):
        quote_order = get_object_or_404(QuoteOrder, quote_order_number=quote_order_number)
        messages.success(request, f"Order successfuly processed! \
            Your order number is {quote_order_number}. A confirmation \
            email will be sent to {quote_order.email}.")
        
        template = 'quotes/quote_checkout_success.html'
        context = {'quote_order': quote_order}
        return render(request, template, context)


class QuoteHistoryView(TemplateView):
    template_name = 'quotes/quote_history.html'

    def get_context_data(self, **kwargs):
        context = super(QuoteHistoryView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        quote_orders = profile.quoteorder_set.all()
        context['quote_orders'] = quote_orders
        return context