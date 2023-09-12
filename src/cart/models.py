from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, pre_save

from .managers import CartManager
from products.models import Product

from .utils import pre_save_total_receiver, m2m_cart_subtotal_receiver, validate_tax

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.FloatField(max_length=120, default=0.0)
    tax = models.FloatField(max_length=120, default=1.0, validators=[validate_tax])
    total = models.FloatField(max_length=120, default=0.0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def cart_have_order(self):
        obj = self.order_set.exists()
        return obj

    def cart_order_status(self):
        if self.cart_have_order():
            obj_status = self.order_set.last().status
        else:
            obj_status = 'No Order'
        return obj_status


m2m_changed.connect(m2m_cart_subtotal_receiver, sender=Cart.products.through)

pre_save.connect(pre_save_total_receiver, sender=Cart)
