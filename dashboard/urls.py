# urls.py
from django.urls import path
from .views import profile_page, profile_update, profile_view

app_name = 'dashboard'

urlpatterns = [
    path('account_centre/', profile_view, name='account_centre'),
    path('profile/', profile_page, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
]
