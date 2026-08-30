from django.urls import path
from . import api_views


urlpatterns = [

    path(
        "products/",
        api_views.ProductListCreateAPIView.as_view(),
        name="api_products"
    ),

    path(
        "products/<int:pk>/",
        api_views.ProductDetailAPIView.as_view(),
        name="api_product_detail"
    ),

]