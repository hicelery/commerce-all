from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductReview, Category

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
