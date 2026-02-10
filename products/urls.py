from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]
