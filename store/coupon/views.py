from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from coupon.serializers import ApplyCouponSerializer
from coupon.services.coupon_service import CouponService


class CouponAPIView(APIView):
    """
    Представление для добавления и удаления купона в корзине
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Save coupon to session cart
        service = CouponService(request=request, instance=serializer.validated_data.get('coupon'))
        service.save_to_cart()

        return Response({'result': True}, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        coupon = request.POST.get('coupon')
        if not coupon:
            return Response({'result': False}, status=HTTP_405_METHOD_NOT_ALLOWED)

        instance = CouponService.get_by_coupon(coupon=coupon)
        if not instance:
            return Response({'result': False}, status=HTTP_404_NOT_FOUND)

        # Delete coupon from session cart
        service = CouponService(request=request, instance=instance)
        service.delete_from_cart()

        return Response({'result': True}, status=HTTP_200_OK)
