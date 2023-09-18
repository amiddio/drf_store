from django.urls import path

from order.views import OrderAPIView

app_name = 'order'

urlpatterns = [
    path('order_create/', OrderAPIView.as_view(), name='create'),
]
