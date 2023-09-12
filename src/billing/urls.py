from django.urls import path

from .views import payment_method_view

urlpatterns = [
    path('payment/', payment_method_view, name='payment_method')

]
