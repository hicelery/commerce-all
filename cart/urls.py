from . import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    # Cart overview
    path('', views.cart_detail, name='view_cart'),

    # Update a cart item (identified by cart and cartitem ids)
    path('<int:cart_id>/update/<int:cartitem_id>/', views.update_cart_item,
         name='update_cart_item'),

    # Add a product to the current session cart (product_id only)
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove a cart item
    path('<int:cart_id>/remove/<int:cartitem_id>/',
         views.remove_from_cart, name='remove_from_cart'),

    # Additional actions used by template (minimal handlers)
    path('clear/', views.clear_cart, name='clear_cart'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),
    path('go-to-checkout/', views.go_to_checkout, name='go-to-checkout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation,
         name='order_confirmation'),

]
