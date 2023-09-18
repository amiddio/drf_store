from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.views import APIView
from rest_framework.response import Response
from cart.cart import Cart
from cart.serializers import CartItemsSerializer, CartUpdateSerializer, CartSerializer
from cart.services.cart_service import CartService


class CartAPIView(APIView):
    """
    Представление корзины
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = Cart(request)
        serializer = CartSerializer(data={
            'items': CartItemsSerializer(cart, many=True).data,
            'total_price': cart.get_total_price(),
            'grand_total_price': cart.get_grand_total_price(),
            'coupon': cart.get_coupon_data()
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            CartService.add_to_cart(request, product_id=data.get('product_id'), qty=data.get('qty'))
            return Response({'result': True}, status=HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'result': False}, status=HTTP_404_NOT_FOUND)

    def patch(self, request, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id:
            return Response({'result': False}, status=HTTP_405_METHOD_NOT_ALLOWED)

        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            CartService.update_qty(request, product_id=product_id, qty=data.get('qty'))
            return Response({'result': True}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'result': False}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id:
            return Response({'result': False}, status=HTTP_405_METHOD_NOT_ALLOWED)

        try:
            CartService.delete(request, product_id=product_id)
            return Response({'result': True}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'result': False}, status=HTTP_404_NOT_FOUND)
