from rest_framework import viewsets

from api.products.serializers import ProductSerializer, ProductFiltersSerializer
from shop.models import Product
from shop.services import filter_products


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """

    queryset = Product.objects.all().order_by("-price")
    serializer_class = ProductSerializer
    permission_classes = []

    def filter_queryset(self, queryset):
        filter_serializer = ProductFiltersSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        return filter_products(queryset, **filter_serializer.validated_data)