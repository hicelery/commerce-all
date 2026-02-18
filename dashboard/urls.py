# urls.py
from django.urls import path
from .views import profile_view

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/account_centre/', profile_view, name='account_centre'),
]
