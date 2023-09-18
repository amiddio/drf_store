from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product
from coupon.models import Coupon


class Order(models.Model):
    """
    Модель заказа
    """

    CREATED = 'CRE'
    PENDING = 'PEN'
    PAID = 'PAD'
    CANCELED = 'CAN'
    STATUS = (
        (CREATED, ' Created'),
        (PENDING, ' Pending'),
        (PAID, ' Paid'),
        (CANCELED, ' Canceled'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, default=CREATED, max_length=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    """
    Модель продукта заказа
    """

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.pk)
