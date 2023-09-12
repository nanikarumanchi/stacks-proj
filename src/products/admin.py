from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'color']
    search_fields = ['category', ]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

