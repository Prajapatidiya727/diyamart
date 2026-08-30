from django.urls import path
from . import views


urlpatterns = [

    # Cart
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # Add product
    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # Remove product
    path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # Increase quantity
    path(
        "increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    # Decrease quantity
    path(
        "decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
]