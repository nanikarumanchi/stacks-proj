from .models import Cart


def cart_product_iem_count(request):
    cart_obj, is_new = Cart.objects.new_or_get(request)
    if is_new:
        count = 0
    else:
        count = cart_obj.products.count()

    context = {
        'count_item_count': count
    }
    return context
