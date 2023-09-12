from django.contrib import admin

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'cart_have_order', 'cart_order_status']

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
