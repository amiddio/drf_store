from rest_framework import serializers
from catalog.models import Product


class CartItemsSerializer(serializers.Serializer):
    """
    Сериалайзер продуктов корзины
    """

    class _InnerProductSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()

        class Meta:
            model = Product
            fields = ('id', 'name')

    qty = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    product = _InnerProductSerializer()


class CartSerializer(serializers.Serializer):
    """
    Сериалайзер корзины
    """

    items = CartItemsSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    grand_total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    coupon = serializers.DictField(allow_empty=True)


class CartUpdateSerializer(serializers.Serializer):
    """
    Сериалайзер обновления корзины
    """

    product_id = serializers.IntegerField()
    qty = serializers.IntegerField(default=1)
