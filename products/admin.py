from django.contrib import admin
from .models import Product, ProductReview, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(Category)
