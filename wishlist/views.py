from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from profiles.models import UserProfile

# Create your views here.
class WishListView(TemplateView):
    template_name = 'wishlist/wish_list.html'

    def get_context_data(self, **kwargs):
        context = super(WishListView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        wishlist = profile.wish_list.all()
        context['wishlist'] = wishlist
        return context
