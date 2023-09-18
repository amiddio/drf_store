from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Coupon(models.Model):
    """
    Модель скидочного купона
    """

    TYPE_FIXED = 'FIX'
    TYPE_PERCENT = 'PRC'
    TYPE_CHOICES = (
        (TYPE_FIXED, 'Fixed'),
        (TYPE_PERCENT, 'Percent'),
    )

    coupon = models.CharField('Coupon', max_length=20, validators=[MinLengthValidator(5)], unique=True)
    coupon_type = models.CharField('Discount type', choices=TYPE_CHOICES, max_length=3)
    value = models.PositiveIntegerField('Discount value')
    total_allowed_apply = models.PositiveIntegerField('Total allowed apply')
    active = models.BooleanField(default=False)
    start_datetime = models.DateTimeField('Valid from')
    end_datetime = models.DateTimeField('Valid to')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, default=None, null=True)
    used = models.ManyToManyField(User, related_name='coupons', blank=True, default=None, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Id: {self.pk}, coupon: {self.coupon}"
