from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
from django.views.generic import TemplateView

# Create your views here.

class DisplayCartView(TemplateView):
    """ A view that displays the contents of the cart """
    
    template_name = "cart/cart.html"


class AddToCart(View):
    """ A view to add items to the cart page """
    def post(self, request, slug):
        quantity = 1
        #gets the redirect url
        redirect_url = request.POST.get('redirect_url')
        #checks if the cart is in the session and then creates an empty dict if it isn't
        cart = request.session.get('cart', {})
        
        #checks if the slug is in the cart dictionary
        if slug in list(cart.keys()):
            messages.error(request, "You already added that item to the cart!")
            return redirect(redirect_url)
            
        else:
            cart[slug] = quantity

        #Adds the amount of that item to its value in the dictionary
        request.session['cart'] = cart
        
        print(request.session['cart'])
        return redirect(redirect_url)


class RemoveFromCart(View):
    """ A view to remove an item from the cart page """
    def post(self, request, slug):
        try:
            #checks if the cart is in the session and then creates an empty dict if it isn't
            cart = request.session.get('cart', {})

            #deletes the item in the list
            cart.pop(slug)

            request.session['cart'] = cart
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)

    
