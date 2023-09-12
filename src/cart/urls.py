from django.urls import path

from .views import CartHome, cart_update, checkout_home, checkout_done, cart_api_view

urlpatterns = [
    path('', CartHome.as_view(), name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    path('success/', checkout_done, name='success'),
    path('api/', cart_api_view, name='api-details'),
]
