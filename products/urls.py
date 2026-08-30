from django.urls import path

from . import views


urlpatterns = [

    # ========================================================
    # HOME
    # ========================================================

    path(
        '',
        views.home,
        name='home'
    ),


    # ========================================================
    # PRODUCTS
    # ========================================================

    path(
        'products/',
        views.product_list,
        name='products'
    ),


    # ========================================================
    # PRODUCT DETAIL
    # ========================================================

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),


    # ========================================================
    # CATEGORIES
    # ========================================================

    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),


    # ========================================================
    # WISHLIST
    # ========================================================

    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    path(
        'wishlist/add/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/remove/<int:product_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),


    # ========================================================
    # NEWSLETTER
    # ========================================================

    path(
        'subscribe/',
        views.subscribe_newsletter,
        name='subscribe_newsletter'
    ),

]