from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    # Products
    path(
        '',
        include('products.urls')
    ),

    # Accounts
    path(
        '',
        include('accounts.urls')
    ),

    # Cart
    path(
        '',
        include('cart.urls')
    ),

    # Orders
    path(
        '',
        include('order.urls')
    ),

    # Wishlist
    path(
        '',
        include('wishlist.urls')
    ),
]


# Media files
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )