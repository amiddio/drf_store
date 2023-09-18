from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from order.serializers import OrderSerializer


class OrderAPIView(APIView):
    """
    Представление оформление заказа
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'result': True}, status=HTTP_201_CREATED)
