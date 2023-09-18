from django.db import transaction
from rest_framework import serializers

from cart.cart import Cart
from coupon.services.coupon_service import CouponService
from order.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериалайзер оформления заказа, с методом сохранения
    """

    user = serializers.SerializerMethodField('get_user')
    total_price = serializers.SerializerMethodField('get_total_price')
    grand_total_price = serializers.SerializerMethodField('get_grand_total_price')
    coupon = serializers.SerializerMethodField('get_coupon')
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self, obj):
        return self.context.get('request').user

    def get_total_price(self, obj):
        cart = Cart(self.context.get('request'))
        return cart.get_total_price()

    def get_grand_total_price(self, obj):
        cart = Cart(self.context.get('request'))
        return cart.get_grand_total_price()

    def get_coupon(self, obj):
        coupon_id = CouponService(request=self.context.get('request')).get_coupon_id()
        if coupon_id:
            return CouponService.get_by_id(pk=coupon_id)
        return None

    def get_status(self, obj):
        return Order.PAID

    def save(self):
        cart = Cart(self.context.get('request'))
        coupon = CouponService(self.context.get('request'), self.data['coupon'])
        with transaction.atomic():
            order = Order.objects.create(**self.data)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], qty=item['qty'])
            cart.clear()
            coupon.delete_from_cart()
