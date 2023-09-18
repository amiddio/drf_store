from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from cart.utils import CartTestCaseMixin
from coupon.models import Coupon


class CouponAPIViewTestCase(CartTestCaseMixin, APITestCase):

    def test_post_request_adding_coupon_to_cart(self):
        response = self._coupon_adding()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals({'result': True}, response.data)
        coupon = Coupon.objects.get(pk=1)
        self.assertEquals(coupon.id, self.client.session.get(settings.COUPON_SESSION_ID))
        self.assertEquals(1, coupon.used.all().count())

    def test_post_request_adding_coupon_to_cart_user_not_allowed(self):
        response = self._coupon_adding(coupon_name='qwerty2')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        error = response.data.get('coupon')
        self.assertEquals([ErrorDetail(string="This coupon not allowed for 'testuser1'", code='invalid')], error)

    def test_delete_request_deleting_coupon_from_cart(self):
        self._coupon_adding()
        url = reverse('coupon:delete')
        response = self.client.delete(url, data={'coupon': 'qwerty'})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals({'result': True}, response.data)
        coupon = Coupon.objects.get(pk=1)
        self.assertFalse(self.client.session.get(settings.COUPON_SESSION_ID))
        self.assertEquals(0, coupon.used.all().count())

    def _coupon_adding(self, coupon_name='qwerty'):
        url = reverse('coupon:apply')
        self._add_product_to_cart(data={'product_id': 1, 'qty': 2})
        return self.client.post(url, data={'coupon': coupon_name})
