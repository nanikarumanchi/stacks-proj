from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm
from billing.models import BillingProfile


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_post or next_ or None
    if form.is_valid():
        billing_profile, is_new = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance = form.save(commit=False)
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type')
            instance.save()
            request.session[request.POST.get('address_type') + '_address_id'] = instance.id
        else:
            print('Error')
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')
