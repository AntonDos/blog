from rest_framework import serializers

from shop.models import STATUS_CHOICES, ORDER_BY_CHOICES


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    image = serializers.ImageField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class ProductFiltersSerializer(serializers.Serializer):
    price__gt = serializers.IntegerField(
        min_value=0,
        label="Price Min",
        required=False,
    )
    price__lt = serializers.IntegerField(
        min_value=0,
        label="Price Max",
        required=False,
    )
    order_by = serializers.ChoiceField(
        choices=ORDER_BY_CHOICES,
        required=False,
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        price__gt = attrs.get("price__gt")
        price__lt = attrs.get("price__lt")
        if price__gt and price__lt and price__gt > price__lt:
            raise serializers.ValidationError("Min price can't be greater than Max price")
        return attrs