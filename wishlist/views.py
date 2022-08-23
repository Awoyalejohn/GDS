from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView, View
from profiles.models import UserProfile
from products.models import Product
from wishlist.models import WishListItem, WishList
from django.contrib import messages

# Create your views here.
class WishListView(TemplateView):
    """ A view to display items in the users wishlist """
    template_name = 'wishlist/wish_list.html'

    def get_context_data(self, **kwargs):
        context = super(WishListView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        wish_list_items = profile.wish_list.wish_list_item.all()
        context['wish_list_items'] = wish_list_items
        return context


class AddToWishList(View):
    """ A view to add items to the user's wishlist """
    def post(self, request, slug):
        try:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            user_wishlist = get_object_or_404(WishList, user_profile=profile)
            product = get_object_or_404(Product, slug=slug)
            wish_list_item, created = WishListItem.objects.get_or_create(wish_list=user_wishlist, product=product)
            if created:
            # A new wislist item object created
                messages.success(request, f"Added {product.name} to your wish list")
            else:
            # wishlist item object already exists
                messages.error(request, f"Error {product.name} already in wishlist!")
            return HttpResponse(status=200)

        except Exception as e:
            messages.error(request, f'Error adding: {e}')
            print(e)
            return HttpResponse(status=500)



class RemoveFromWishList(View):
    """ A view to remove an item from the user's wishlist """
    def post(self, request, slug):
        try:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            user_wishlist = get_object_or_404(WishList, user_profile=profile)
            product = get_object_or_404(Product, slug=slug)
            wish_list_item = get_object_or_404(WishListItem, wish_list=user_wishlist, product=product)
            redirect_url = request.POST.get('redirect_url')
            wish_list_item.delete()
            messages.success(request, f'Removed {product.name} from wishlist')
            return HttpResponse(status=200)

        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)


        
