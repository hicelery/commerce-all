from . import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    # category route placed after pr>oduct routes to avoid catching 'product' literalpath('checkout/', views.checkout, name='checkout'),
    path('', views.cart_detail, name='view_cart'),

    # maybe move these to product urls? but then would need to pass cart_id in the url which seems weird
    path('<int:cart_id>/update/<int:product_id>/', views.update_cart_item,
         name='update_cart_item'),

    path('<int:cart_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('<int:cart_id>/remove/<int:product_id>/',
         views.remove_from_cart, name='remove_from_cart'),

]
