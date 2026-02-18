from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(CartItem)


@admin.register(Cart)
class CartAdmin(SummernoteModelAdmin):

    list_display = ('cart_id', 'user', 'created_at', 'updated_at', 'is_active')
    search_fields = ['user__username']
    list_filter = ('user', 'created_at', 'is_active')


@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    list_display = ('user', 'order_id',
                    'total_price', 'created_at')
    list_filter = ('user', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(SummernoteModelAdmin):
    list_display = ('order_id', 'product', 'quantity', 'price')
    list_filter = ('order_id', 'product')
