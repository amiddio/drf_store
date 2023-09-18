from collections import OrderedDict
from rest_framework.exceptions import ValidationError

from cart.cart import Cart
from cart.serializers import CartUpdateSerializer, CartSerializer, CartItemsSerializer
from cart.utils import CartTestCaseMixin
from rest_framework.test import APITestCase
from django.test import TestCase


class CartItemsSerializerTestCase(CartTestCaseMixin, APITestCase):

    def test_data_fields(self):
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        self._add_product_to_cart(data={'product_id': 2, 'qty': 2})

        expected_data = [
            OrderedDict([('qty', 2), ('price', '17.50'), ('total_price', '35.00'),
                         ('product', OrderedDict([('id', 1), ('name', 'Product 1')]))]),
            OrderedDict([('qty', 2), ('price', '30.99'), ('total_price', '61.98'),
                         ('product', OrderedDict([('id', 2), ('name', 'Product 2')]))])
        ]

        data = self._get_cart_serializer_data()
        self.assertEquals(expected_data, data)


class CartUpdateSerializerTestCase(TestCase):

    def test_data_fields(self):
        serializer = CartUpdateSerializer(data={'product_id': 1, 'qty': 5})
        serializer.is_valid()
        expected_data = {'product_id': 1, 'qty': 5}
        self.assertEquals(expected_data, serializer.data)

        serializer = CartUpdateSerializer(data={'product_id': 1})
        serializer.is_valid()
        expected_data = {'product_id': 1, 'qty': 1}
        self.assertEquals(expected_data, serializer.data)

    def test_wrong_data_fields(self):
        with self.assertRaises(ValidationError):
            serializer = CartUpdateSerializer(data={'product_id_not_sent': 1, 'qty': 5})
            serializer.is_valid(raise_exception=True)


class CartSerializerTestCase(CartTestCaseMixin, APITestCase):

    def test_data_fields(self):
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})

        cart = Cart(self.client)
        serializer = CartSerializer(data={
            'items': CartItemsSerializer(cart, many=True).data,
            'total_price': cart.get_total_price(),
            'grand_total_price': cart.get_grand_total_price(),
            'coupon': cart.get_coupon_data()
        })
        serializer.is_valid(raise_exception=True)

        expected_data = {
            'items': [OrderedDict([('qty', 2), ('price', '17.50'), ('total_price', '35.00'),
                                   ('product', OrderedDict([('id', 1), ('name', 'Product 1')]))])],
            'total_price': '35.00', 'grand_total_price': '35.00', 'coupon': {}
        }
        self.assertEquals(expected_data, serializer.data)
