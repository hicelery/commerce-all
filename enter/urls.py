from . import views
from django.urls import path

app_name = 'enter'

urlpatterns = [
    # Cart overview
    path('', views.enter_page, name='enter'),
]
