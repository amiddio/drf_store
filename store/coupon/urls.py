from django.urls import path

from coupon.views import CouponAPIView

app_name = 'coupon'

urlpatterns = [
    path('apply_coupon/', CouponAPIView.as_view(), name='apply'),
    path('delete_coupon/', CouponAPIView.as_view(), name='delete'),
]
