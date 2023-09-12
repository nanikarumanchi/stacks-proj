import stripe
from django.shortcuts import render

STRIPE_PUB_KEY = "pk_test_Y2xruzYt8ElRlr4iG55yCavU00Y2QXIutF"
stripe.api_key = 'sk_test_UJlhQeQ2oE42oPatWBDFaHyR00SfHwZ3q7'


def payment_method_view(request):
    context = {
        'publish_key': STRIPE_PUB_KEY
    }
    if request.method == "POST":
        print(request.POST)

    return render(request, 'billing/payment_method.html', context)
