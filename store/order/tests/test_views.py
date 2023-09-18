from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cart.utils import CartTestCaseMixin


class OrderAPIViewTestCase(CartTestCaseMixin, APITestCase):

    def test_post_request(self):
        # Added product to cart
        data = {'product_id': 1, 'qty': 2}
        url = reverse('cart:list')
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals({'result': True}, response.data)
        # Save order
        url = reverse('order:create')
        data = {
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'j.dow@gmail.com',
            'address': 'Luxery, #789 st.',
            'postal_code': '0589',
            'city': 'LA',
            'country': 'USA',
        }
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals({'result': True}, response.data)
