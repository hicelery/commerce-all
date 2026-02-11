from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from requests import post
from .models import Product, ProductReview, Category
from .forms import ReviewForm

# Create your views here.


# Product list view with optional category filter.
# Inputs: request, category_name (default to null so as not to break non-category filtered view)
# If category_name is provided, filter products by category name (case-insensitive).


def ProductList(request, category_name=None):
    qs = Product.objects.all()
    category_key = category_name or request.GET.get('category_name')
    if category_key:
        qs = qs.filter(category__name__iexact=category_key)
        # from django.core.paginator import (
        #     Paginator, EmptyPage, PageNotAnInteger
        # )
        #
        # # Use paginator to paginate queryset for template controls.
        # paginator = Paginator(qs, 24)
        # page = request.GET.get('page', 1)
        # try:
        #     page_obj = paginator.page(page)
        # except PageNotAnInteger:
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     page_obj = paginator.page(paginator.num_pages)

    context = {
        'products': qs,
        'categories': Category.objects.all(),

    }
    return render(request, 'products/product_list.html', context)


# Product detail view with review form handling.
#
# Inputs: request, product_id (from URL)
# Output: All product details, reviews, and review form to detail template.
#
# Retrieves the product and its reviews
# handles POST requests for new reviews
# renders the product

def product_detail(request, product_id):

    # Get the product
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, product_id=product_id)
    reviews = product.reviews.order_by("-created_at")
    review_count = product.reviews.filter(approved=True).count()

    # Post request for comment forms
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST, user=request.user)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            # Only staff may set approved via the form
            if request.user.is_authenticated and request.user.is_staff:
                review.approved = review_form.cleaned_data.get(
                    'approved', False)
            else:
                review.approved = False
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Review submitted and awaiting approval'
            )
            return HttpResponseRedirect(reverse('products:product_detail', args=[product.product_id]))
        review_form = ReviewForm(user=request.user)

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

# Review Edit
# Chains into reviews js
#
# Inputs: request, product_id (int), review_id (from URL)
# Output: Edits the review if the user is the author or staff, then redirects to product detail page.


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
        review_form = ReviewForm(
            data=request.POST, instance=review, user=request.user)
        # allow the author or staff to edit
        if (review.user == request.user or (request.user.is_authenticated and request.user.is_staff)) and review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            # if staff, accept the approved flag, otherwise ensure edits reset approval
            if request.user.is_authenticated and request.user.is_staff:
                review.approved = review_form.cleaned_data.get(
                    'approved', False)
            else:
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

# Review Delete
#
# Inputs: request, product_id (int), review_id (from URL)
# Output: none
# Deleted review entry then redirects to product detail page.
#
# reviews js handles confirmation and chaining to this view


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
