from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.class OrderAdmin(admin.ModelAdmin):
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_subtotal',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'discount', 'order_subtotal',
                       'total',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'discount',
              'order_subtotal', 'total',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_subtotal', 'discount',
                    'total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
