from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(),
         name='product_detail'),
    path('product/<int:product_id>/review/',
         views.product_detail, name='review'),
]
