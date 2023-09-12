from django.urls import path

from .views import login_page_fbv, logout_fbv, register_fbv, guest_view

urlpatterns = [
    path('login/', login_page_fbv, name='account_login'),
    path('logout/', logout_fbv, name='account_logout'),
    path('register/', register_fbv, name='account_register'),
    path('register/guest/', guest_view, name='account_guest'),
]
