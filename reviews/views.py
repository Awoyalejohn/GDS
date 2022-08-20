from django.views.generic.edit import UpdateView
from .models import Review
from .forms import ReviewForm


# Create your views here.

# Redirect mixin form stackoverflow post
# https://stackoverflow.com/questions/62626660/redirect-back-to-previous-page-django
class RedirectToPreviousMixin:
    """ A mixin that allows users to redirect back to a previous page when form is submitted"""
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']
class UpdateReview(RedirectToPreviousMixin, UpdateView):
    """ A view to edit a product review"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'
    success_message = 'Successfully Updated review!'
    error_message = 'Failed to update review. Please ensure the form is valid.'

    def get_object(self):
        review = Review.objects.get(id=self.kwargs['review_id'])
        return review