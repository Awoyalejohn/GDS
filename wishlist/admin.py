from django.contrib import admin
from .models import WishList, WishListItem


class WishListItemAdminInline(admin.TabularInline):
    model = WishListItem


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    inlines = (WishListItemAdminInline,)
