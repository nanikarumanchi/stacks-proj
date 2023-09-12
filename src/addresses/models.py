from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('shipping', 'Shipping'),
    ('billing', 'Billing')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, default='billing', choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)
