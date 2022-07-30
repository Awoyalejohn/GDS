from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart_items = []
    subtotal = 0
    product_count = 0
    cart = request.session.get('cart',{})

    for slug, quantity in cart.items():
        product = get_object_or_404(Product, slug=slug)
        subtotal += product.price
        product_count += quantity
        cart_items.append({
            'slug': slug,
            'quantity': quantity,
            'product': product,
        })

    if subtotal > settings.DISCOUNT_THRESHOLD:
        discount = subtotal * Decimal(settings.DISCOUNT_PERCENTAGE / 100)
        discount_delta = 0
        
    else:
        discount = 0
        discount_delta = settings.DISCOUNT_THRESHOLD - subtotal

    total = subtotal - discount

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'product_count': product_count,
        'discount': discount,
        'discount_delta': discount_delta,
        'discount_threshold': settings.DISCOUNT_THRESHOLD,
        'discount_percentage': settings.DISCOUNT_PERCENTAGE,
        'total': total,
        
    }

    return context