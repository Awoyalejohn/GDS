from decimal import Decimal
from django.conf import settings

def cart_contents(request):
    cart_items = []
    subtotal = 0
    product_count = 0

    if subtotal < settings.DISCOUNT_THRESHOLD:
        discount = 0
        discount_delta = settings.DISCOUNT_THRESHOLD - subtotal
    else:
        discount = subtotal * Decimal(settings.DISCOUNT_PERCENTAGE / 100)

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