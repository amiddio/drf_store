# Generated by Django 4.2.4 on 2023-08-27 09:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='used',
            field=models.ManyToManyField(related_name='coupons', to=settings.AUTH_USER_MODEL),
        ),
    ]
