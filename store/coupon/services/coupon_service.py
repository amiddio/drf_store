from django.conf import settings
from django.db.models import Count

from coupon.models import Coupon


class CouponService:

    def __init__(self, request, instance=None):
        self.user = request.user
        self.session = request.session
        self.instance = instance

    def save_to_cart(self):
        self.instance.used.add(self.user)
        self.session[settings.COUPON_SESSION_ID] = self.instance.id
        self._session_modified()

    def delete_from_cart(self):
        if self.session.get(settings.COUPON_SESSION_ID, None):
            self.instance.used.remove(self.user)
            del self.session[settings.COUPON_SESSION_ID]
        self._session_modified()

    def _session_modified(self):
        self.session.modified = True

    def get_coupon_id(self):
        if self.session.get(settings.COUPON_SESSION_ID, None):
            return self.session.get(settings.COUPON_SESSION_ID)
        return None

    @staticmethod
    def get_by_coupon(coupon: str) -> Coupon:
        coupon = coupon.lower().strip()
        return Coupon.objects.filter(coupon__iexact=coupon).annotate(total_used=Count('used')).first()

    @staticmethod
    def get_by_id(pk: int) -> Coupon:
        return Coupon.objects.get(pk=pk)
