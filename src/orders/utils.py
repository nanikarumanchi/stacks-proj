from ab_stacks_main.utils import random_string_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('paid', 'Paid'),
    ('canceled', 'Canceled'),
)


def unique_order_id_generator(instance):
    order_id = random_string_generator().upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_id



