from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('products', views.ProductList, name='home'),
    path('products/product/<int:product_id>/',
         views.product_detail, name='product_detail'),
    path('products/product/<int:product_id>/review_edit/<int:review_id>/',
         views.review_edit, name='review_edit'),
    path('products/product/<int:product_id>/review_delete/<int:review_id>/',
         views.review_delete, name='review_delete'),
    # category route placed after product routes to avoid catching 'product' literal
    path('products/<str:category_name>/',
         views.ProductList, name='category'),
]
