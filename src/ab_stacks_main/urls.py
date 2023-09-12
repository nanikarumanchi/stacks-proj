from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='account')),
    path('', include(('home_details.urls', 'home_details'), namespace='home_detail')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('billing/', include(('billing.urls', 'billing'), namespace='billing')),
    path('address/', include(('addresses.urls', 'addresses'), namespace='addresses')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
