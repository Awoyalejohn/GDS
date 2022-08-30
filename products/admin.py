from atexit import register
from django.contrib import admin
from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price", "rating", "image")
    prepopulated_fields = {"slug": ("name",)}
