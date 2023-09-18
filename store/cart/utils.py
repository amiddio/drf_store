from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token

from cart.cart import Cart
from cart.serializers import CartItemsSerializer
from catalog.models import Product
from coupon.models import Coupon


class CartTestCaseMixin:
    """Вспомогательные методы для юниттестов"""

    @classmethod
    def setUpTestData(cls):
        Product.actived.create(name='Product 1', qty=10, price=17.50)
        Product.actived.create(name='Product 2', qty=25, price=30.99)
        User.objects.create_user(username='testuser1', password='12345')
        user2 = User.objects.create_user(username='testuser2', password='12345')
        Coupon.objects.create(
            coupon='qwerty',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1)
        )
        Coupon.objects.create(
            coupon='qwerty2',
            coupon_type=Coupon.TYPE_PERCENT,
            value=10,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1),
            user=user2
        )
        Coupon.objects.create(
            coupon='qwerty_fix',
            coupon_type=Coupon.TYPE_FIXED,
            value=20,
            total_allowed_apply=1,
            active=True,
            start_datetime=timezone.now() - timedelta(1),
            end_datetime=timezone.now() + timedelta(1)
        )

    def setUp(self):
        self._user_login()

    def _user_login(self):
        self.client.post(
            '/api/v1/auth/token/login/',
            data={'username': 'testuser1', 'password': '12345'}
        )
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def _add_product_to_cart(self, data):
        url = reverse('cart:list')
        self.client.post(url, data=data)

    def _get_cart_serializer_data(self):
        cart = Cart(self.client)
        serializer = CartItemsSerializer(cart, many=True)
        return serializer.data
