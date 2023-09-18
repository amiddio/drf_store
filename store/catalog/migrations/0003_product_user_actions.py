# Generated by Django 4.2.4 on 2023-08-20 09:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_alter_category_options_productuserrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_actions',
            field=models.ManyToManyField(through='catalog.ProductUserRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]