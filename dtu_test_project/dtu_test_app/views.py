from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from django_tenants_url.permissions import IsTenantAllowedOrPublic

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductTenantListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsTenantAllowedOrPublic]

    def get_queryset(self):
        return Product.objects.all()
