from django.contrib import admin
from .models import WishList, WishListItem

# Register your models here.
class WishListItemAdminInline(admin.TabularInline):
    model = WishListItem
  
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    inlines = (WishListItemAdminInline,)

