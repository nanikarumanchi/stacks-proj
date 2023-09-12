from django.urls import path

from .views import checkout_address_create_view
urlpatterns = [
    path('', checkout_address_create_view, name='create_address')
]