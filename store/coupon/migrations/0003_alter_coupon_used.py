# Generated by Django 4.2.4 on 2023-08-27 09:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0002_coupon_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='used',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='coupons', to=settings.AUTH_USER_MODEL),
        ),
    ]
