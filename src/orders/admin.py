from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cart', 'get_cart_user', 'status', 'active']

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
