from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from requests import post
from .models import Product, ProductReview, Category
from .forms import ReviewForm

# Create your views here.

# update to add reviews to the product list view,


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 24


# does this need a get_context_data method to add the reviews to the context?
# does this need a post method to handle the review form submission?
# does this need to call a template?


def product_detail(request, product_id):

    # Get the product
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, product_id=product_id)
    reviews = product.reviews.order_by("-created_at")
    review_count = product.reviews.filter(approved=True).count()

    # Post request for comment forms
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.approved = False
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Review submitted and awaiting approval'
            )
            return HttpResponseRedirect(reverse('products:product_detail', args=[product.product_id]))
    review_form = ReviewForm()

    context = {
        "product": product,
        "reviews": reviews,
        "review_count": review_count,
        "review_form": review_form, }

    return render(
        request,
        "products/product_detail.html",
        context,
    )


def review_edit(request, product_id, review_id):
    """View to edit a comment.
    Needs js to reopen form
    """
    if request.method == "POST":
        # Get the product with review attached
        queryset = Product.objects.all()
        product = get_object_or_404(
            queryset, product_id=product_id)
        # get the review to edit
        review = get_object_or_404(ProductReview, pk=review_id)
        review_form = ReviewForm(data=request.POST, instance=review)
        # check if the user is the author of the comment and form valid
        if review.user == request.user and review_form.is_valid():

            # If the user is the author, update the comment with the new content and save it
            review = review_form.save(commit=False)
            review.product = product
            review.approved = False
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Review updated successfully'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'You are not authorized to edit this review'
            )
        # Redirect the user back to the post detail page
        return HttpResponseRedirect(reverse('products:product_detail', args=[product.product_id]))


def review_delete(request, product_id, review_id):
    """
    view to delete review
    """
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, product_id=product_id)
    review = get_object_or_404(ProductReview, pk=review_id)

    if review.user == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own reviews!')

    return HttpResponseRedirect(reverse('products:product_detail', args=[product.product_id]))
