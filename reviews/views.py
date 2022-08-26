from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.edit import View
from django.http import HttpResponseRedirect
from .models import Review
from products.models import Product
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg



class UpdateReview(LoginRequiredMixin, View):
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
        product = review.product
        reviews = product.product_review.all()
        slug = review.product.slug
        print(slug)
        form = ReviewForm(self.request.POST, instance=review)
        if form.is_valid():
            form.save()
            avg_reviews = reviews.aggregate(Avg('rating')) 
            product.rating = avg_reviews['rating__avg']
            product.save()
            messages.success(request, 'Review was updated successfully')
            return HttpResponseRedirect(reverse('product_detail', args=[slug]))


class DeleteReview(LoginRequiredMixin, View):
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
        product = review.product
        reviews = product.product_review.all()
        slug = review.product.slug
        print(slug)
        review.delete()
        avg_reviews = reviews.aggregate(Avg('rating')) 
        product.rating = avg_reviews['rating__avg']
        product.save()
        messages.success(request, 'Review has been deleted')
        return HttpResponseRedirect(reverse('product_detail', args=[slug]))



