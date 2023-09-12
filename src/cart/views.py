from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from cart.models import Cart
from billing.models import BillingProfile
from products.models import Product
from orders.models import Order
from accounts.forms import GuestForm
from addresses.forms import AddressForm
from addresses.models import Address


def cart_api_view(request):
    cart_obj, is_cart_created = Cart.objects.new_or_get(request)
    products = [
        {
            'id': x.id,
            'url': x.get_absolute_url(),
            'name': x.title,
            'price': x.final_price}
        for x in cart_obj.products.all()
    ]
    cart_data = {
        'product': products,
        'cart_subtotal': cart_obj.subtotal,
        'cart_total': cart_obj.total,
    }
    return JsonResponse(cart_data)


class CartHome(TemplateView):
    template_name = 'cart/home.html'
    model = Cart

    def get(self, request, *args, **kwargs):
        cart_obj, is_cart_created = Cart.objects.new_or_get(request)
        context = {
            'cart': cart_obj
        }
        return render(request, self.template_name, context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product doesnt exist')
        cart_obj, is_cart_created = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            is_added = False
        else:
            cart_obj.products.add(product_obj)
            is_added = True
        request.session['cart_product_count'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                'added': is_added,
                'removed': not is_added,
                'cart_item_count': cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, is_cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    if is_cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    billing_profile, is_billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, is_new_order = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id is not None:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
    # check out
    if request.method == 'POST':
        is_payment_done = order_obj.check_done()
        if is_payment_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_product_count'] = 0
            return redirect('cart:success')
    context = {
        "object": order_obj,
        'billing_profile': billing_profile,
        'guest_form': guest_form,
        'address_form': address_form,
    }
    return render(request, 'cart/checkout.html', context)


def checkout_done(request):
    return render(request, 'cart/checkout_done.html', {})
