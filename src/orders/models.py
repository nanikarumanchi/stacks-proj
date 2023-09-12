from django.db import models
from django.db.models.signals import pre_save, post_save

from cart.models import Cart
from billing.models import BillingProfile
from addresses.models import Address

from .managers import OrderManager
from .utils import ORDER_STATUS_CHOICES, unique_order_id_generator


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='shipping_address')
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='billing_address')
    order_id = models.CharField(max_length=120, unique=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_charges = models.FloatField(max_length=120, default=45.0)
    total = models.FloatField(max_length=120, default=0)
    active = models.BooleanField(default=True)
    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def get_cart_user(self):
        return self.cart.user

    def update_total(self):
        cart_total = self.cart.total
        shipping_charges = self.shipping_charges
        total = cart_total + shipping_charges
        self.total = total
        self.save()
        return total

    def check_done(self):
        if self.billing_profile and self.shipping_address and self.billing_address and self.total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_order_id_create_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart, active=True).exclude(billing_profile=instance.billing_profile)
    print(qs)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_order_id_create_receiver, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    print('created in cart_total func', created)
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists():
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print('created in order func', created)
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
