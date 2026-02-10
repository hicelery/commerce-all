from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from requests import post
from .models import Product, ProductReview, Category
from .forms import ReviewForm

# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 24


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

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
            return HttpResponseRedirect(reverse('products:product_detail', kwargs={'product_id': product.product_id}))
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
