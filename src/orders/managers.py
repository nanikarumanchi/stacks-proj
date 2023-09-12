from django.db import models


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        is_new_order = False
        order_qs = self.get_queryset().filter(billing_profile=billing_profile,
                                              cart=cart_obj, active=True,
                                              status='created')
        if order_qs.exists():
            order_obj = order_qs.first()
        else:
            order_obj = self.model.objects.create(cart=cart_obj, billing_profile=billing_profile)
            is_new_order = True

        return order_obj, is_new_order
