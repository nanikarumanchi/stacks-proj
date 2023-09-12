import stripe
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from billing.managers import BillingManager

User = get_user_model()

stripe.api_key = 'sk_test_UJlhQeQ2oE42oPatWBDFaHyR00SfHwZ3q7'


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    objects = BillingManager()

    def __str__(self):
        return self.email

    def user_username(self):
        if self.user:
            return self.user.username.capitalize()
        else:
            return '-'


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(email=instance.email)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
