from django.urls import path, include
from cart.views import CartAPIView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name='list'),
    path('cart/<int:product_id>/', CartAPIView.as_view(), name='detail'),
]
