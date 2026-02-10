from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(),
         name='product_detail'),
]
