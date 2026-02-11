from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review_edit/<int:review_id>/',
         views.review_edit, name='review_edit'),
    path('product/<int:product_id>/review_delete/<int:review_id>/',
         views.review_delete, name='review_delete'),

]
