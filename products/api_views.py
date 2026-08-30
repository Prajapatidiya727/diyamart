from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product
from .serializers import ProductSerializer



class ProductListCreateAPIView(ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer