from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Product

from cart.models import Cart


class ProductListView(ListView):
    template_name = 'products/list_view.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        cart_obj, is_cart_created = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart_obj, is_cart_created = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
