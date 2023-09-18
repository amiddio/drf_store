from django.utils import timezone
from rest_framework import serializers

from coupon.services.coupon_service import CouponService


class ApplyCouponSerializer(serializers.Serializer):
    """
    Сериалайзер с кастомной валидацией применения купона в корзине
    """

    coupon = serializers.CharField()

    def validate(self, data):
        coupon = CouponService.get_by_coupon(coupon=data.get('coupon'))
        if not coupon:
            raise serializers.ValidationError({'coupon': "Coupon not exist"})
        if not coupon.active:
            raise serializers.ValidationError({'coupon': "Coupon disabled"})
        if not (coupon.start_datetime < timezone.now() < coupon.end_datetime):
            raise serializers.ValidationError({'coupon': "Coupon expired or not allowed"})
        if coupon.total_used == coupon.total_allowed_apply:
            raise serializers.ValidationError({'coupon': "Coupon reached usage limit"})
        if coupon.user and coupon.user.id != self.context['request'].user.id:
            raise serializers.ValidationError({
                'coupon': f"This coupon not allowed for '{self.context['request'].user.username}'"
            })

        data['coupon'] = coupon
        return data
