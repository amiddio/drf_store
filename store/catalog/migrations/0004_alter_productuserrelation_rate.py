# Generated by Django 4.2.4 on 2023-08-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product_user_actions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productuserrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
