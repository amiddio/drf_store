from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework.exceptions import ValidationError, ErrorDetail

from cart.utils import CartTestCaseMixin
from coupon.models import Coupon
from coupon.serializers import ApplyCouponSerializer


class ApplyCouponSerializerTestCase(TestCase):

    def test_validation_coupon_not_exist(self):
        Coupon.objects.create(
            coupon='qwerty',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1)
        )
        serializer = ApplyCouponSerializer(data={'coupon': 'qwerty1'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        error = serializer.errors.get('coupon')
        self.assertEquals([ErrorDetail(string='Coupon not exist', code='invalid')], error)

    def test_validation_coupon_not_active(self):
        Coupon.objects.create(
            coupon='qwerty',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=False,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1)
        )
        serializer = ApplyCouponSerializer(data={'coupon': 'qwerty'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        error = serializer.errors.get('coupon')
        self.assertEquals([ErrorDetail(string='Coupon disabled', code='invalid')], error)

    def test_validation_coupon_expired(self):
        Coupon.objects.create(
            coupon='qwerty',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(2),
            end_datetime=timezone.now() - timedelta(1)
        )
        serializer = ApplyCouponSerializer(data={'coupon': 'qwerty'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        error = serializer.errors.get('coupon')
        self.assertEquals([ErrorDetail(string='Coupon expired or not allowed', code='invalid')], error)

    def test_validation_coupon_total_used(self):
        user = User.objects.create_user(username='testuser1', password='12345')
        coupon = Coupon.objects.create(
            coupon='qwerty',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1)
        )
        coupon.used.add(user)
        serializer = ApplyCouponSerializer(data={'coupon': 'qwerty'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        error = serializer.errors.get('coupon')
        self.assertEquals([ErrorDetail(string='Coupon reached usage limit', code='invalid')], error)
