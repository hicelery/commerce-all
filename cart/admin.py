from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Cart)
class CartAdmin(SummernoteModelAdmin):

    list_display = ('cart_id', 'user', 'created_at', 'updated_at')
    search_fields = ['user__username']
    list_filter = ('user', 'created_at')
