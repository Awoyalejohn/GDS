from atexit import register
from django.contrib import admin
from products.models import Category, Product

# Register your models here.
admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'rating', 'image')
    prepopulated_fields = {"slug": ("name",)}


