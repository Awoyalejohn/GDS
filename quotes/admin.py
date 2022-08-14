from django.contrib import admin
from quotes.models import QuoteRequest, QuoteOrder

# Register your models here.
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'submitted')


@admin.register(QuoteOrder)
class QuoteOrderAdmin(admin.ModelAdmin):
    list_display = ('quote_request_name', 'user', 'submitted')
    readonly_fields = ('quote_request_name', 'type', 'size', 'description',
                       'subtotal', 'discount', 'total', 'stripe_pid')
