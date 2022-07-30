from django.views.generic import TemplateView

# Create your views here.

class DisplayCartView(TemplateView):
    """ A view that displays the contents of the cart """
    
    template_name = "cart/cart.html"
