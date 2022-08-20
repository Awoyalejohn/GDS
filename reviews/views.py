from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.edit import View
from django.http import HttpResponseRedirect
from .models import Review
from .forms import ReviewForm
from django.contrib import messages


class UpdateReview(View):
    """ A view to edit a product review """
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        slug = review.product.slug
        print(slug)
        form = ReviewForm(instance=review)
        context = {'review': review, 'form':form}
        template = 'reviews/edit_review.html'
        return render(request, template, context)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        slug = review.product.slug
        print(slug)
        form = ReviewForm(self.request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review was updated successfully')
            return HttpResponseRedirect(reverse('product_detail', args=[slug]))


class DeleteReview(View):
    """ A view for users to delete reviews """
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        slug = review.product.slug
        print(slug)
        context = {'review': review}
        template = 'reviews/delete_review.html'
        return render(request, template, context)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        slug = review.product.slug
        print(slug)
        review.delete()
        messages.success(request, 'Review has been deleted')
        return HttpResponseRedirect(reverse('product_detail', args=[slug]))



