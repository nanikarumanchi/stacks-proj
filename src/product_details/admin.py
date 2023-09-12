from django.contrib import admin

from .mobiles.models import Mobile
from .laptops.models import Laptop


class MobileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'final_price']

    class Meta:
        model = Mobile


class LaptopAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'final_price']

    class Meta:
        model = Laptop


admin.site.register(Mobile, MobileAdmin)
admin.site.register(Laptop, LaptopAdmin)
