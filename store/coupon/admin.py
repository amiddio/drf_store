from django.contrib import admin

from coupon.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'coupon_type', 'value', 'start_datetime', 'end_datetime', 'active')
