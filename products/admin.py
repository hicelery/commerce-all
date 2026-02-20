from django.contrib import admin
from .models import Product, ProductImage, ProductReview, Category, ProductSize, ProductDiscount, DiscountCode
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):

    list_display = ('brand', 'name',
                    'category', 'price', 'created_at', 'size', 'colour',)
    search_fields = ['name', 'description', 'brand', 'category']
    list_filter = ('name', 'brand', 'category', 'created_at')
    summernote_fields = ('description')


@admin.register(ProductReview)
class ProductReviewAdmin(SummernoteModelAdmin):

    list_display = ('product', 'user', 'rating', 'approved', 'created_at')
    search_fields = ['product__name', 'user__username', 'comment']
    list_filter = ('user', 'approved')
    summernote_fields = ('comment')


admin.site.register(Category)

admin.site.register(ProductSize)

admin.site.register(ProductImage)

admin.site.register(ProductDiscount)


@admin.register(DiscountCode)
class DiscountCodeAdmin(SummernoteModelAdmin):

    list_display = ('code', 'discount_percentage', 'category',
                    'max_uses', 'start_date', 'end_date', 'created_at')
    list_filter = ('code', 'discount_percentage', 'category',
                   'start_date', 'end_date', 'created_at')
    search_fields = ['start_date', 'end_date',
                     'discount_percentage', 'category']
