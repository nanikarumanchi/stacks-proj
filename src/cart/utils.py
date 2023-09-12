from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def m2m_cart_subtotal_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        cart_subtotal = 0
        for product in products:
            cart_subtotal += product.final_price

        instance.subtotal = cart_subtotal
        instance.save()


def pre_save_total_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        if instance.tax == 1:
            instance.total = float(instance.subtotal)
        else:
            instance.total = float(instance.subtotal) + ((float(instance.subtotal) * float(instance.tax)) / 100)
    else:
        instance.total = 0


def validate_tax(value):
    if value == 0:
        raise ValidationError(
            _('%(value) can\'t be TAX. if not set as 1 '),
            params={'value': value},
        )
