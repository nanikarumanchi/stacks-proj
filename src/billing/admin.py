from django.contrib import admin

from .models import BillingProfile


class BillingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user_username', 'customer_id']

    class Meta:
        model = BillingProfile


admin.site.register(BillingProfile, BillingAdmin)
