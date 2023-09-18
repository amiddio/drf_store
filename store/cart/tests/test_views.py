from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cart.utils import CartTestCaseMixin


class CartAPIViewTestCase(CartTestCaseMixin, APITestCase):

    def test_auth(self):
        url = reverse('cart:list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], response.data.get('items'))

    def test_get_request(self):
        url = reverse('cart:list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], response.data.get('items'))

    def test_get_request_list_products(self):
        url = reverse('cart:list')
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        self._add_product_to_cart(data={'product_id': 2, 'qty': 3})
        response = self.client.get(url)
        cart_data = self._get_cart_serializer_data()
        self.assertEquals(cart_data, response.data.get('items'))
        self.assertTrue(2, len(cart_data))
        total_price = Decimal(response.data.get('total_price'))
        grand_total_price = Decimal(response.data.get('grand_total_price'))
        self.assertEquals(total_price, grand_total_price)

    def test_post_request(self):
        url = reverse('cart:list')
        data = {'product_id': 1, 'qty': 2}
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals({'result': True}, response.data)

    def test_post_request_not_exist_product(self):
        url = reverse('cart:list')
        data = {'product_id': 100, 'qty': 3}
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEquals({'result': False}, response.data)

    def test_patch_request(self):
        url = reverse('cart:detail', args=['1'])
        # Added a product to cart
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        cart_data = self._get_cart_serializer_data()
        self.assertEquals(2, cart_data[0]['qty'])
        # Changed qty of added product
        data = {'product_id': 1, 'qty': 3}
        response = self.client.patch(url, data=data)
        self.assertEquals({'result': True}, response.data)
        # Checked qty value again
        cart_data = self._get_cart_serializer_data()
        self.assertEquals(3, cart_data[0]['qty'])

    def test_delete_request(self):
        url = reverse('cart:detail', args=['1'])
        # Added a product to cart
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        cart_data = self._get_cart_serializer_data()
        self.assertEquals(1, len(cart_data))
        response = self.client.delete(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals({'result': True}, response.data)
        # Checked cart again
        cart_data = self._get_cart_serializer_data()
        self.assertEquals(0, len(cart_data))

    def test_coupon_discount_percentage_calculation(self):
        url = reverse('cart:list')
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        self._add_product_to_cart(data={'product_id': 2, 'qty': 3})
        self._coupon_adding()
        response = self.client.get(url).data
        total_price = Decimal(response.get('total_price'))
        grand_total_price = Decimal(response.get('grand_total_price'))
        coupon_value = Decimal(response.get('coupon')['value'])
        self.assertTrue(grand_total_price == total_price - coupon_value)
        self.assertTrue(response.get('coupon')['name'] == 'qwerty')
        self.assertTrue(response.get('coupon')['label'] == '-10%')

    def test_coupon_discount_fix_calculation(self):
        url = reverse('cart:list')
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        self._add_product_to_cart(data={'product_id': 2, 'qty': 3})
        self._coupon_adding(coupon_name='qwerty_fix')
        response = self.client.get(url).data
        total_price = Decimal(response.get('total_price'))
        grand_total_price = Decimal(response.get('grand_total_price'))
        coupon_value = Decimal(response.get('coupon')['value'])
        self.assertTrue(grand_total_price == total_price - coupon_value)
        self.assertTrue(response.get('coupon')['name'] == 'qwerty_fix')
        self.assertTrue(response.get('coupon')['label'] == '-20')

    def _coupon_adding(self, coupon_name='qwerty'):
        url = reverse('coupon:apply')
        return self.client.post(url, data={'coupon': coupon_name})
