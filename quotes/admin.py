from django.contrib import admin
from quotes.models import QuoteRequest

# Register your models here.
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'submitted', 'quote_order_number')