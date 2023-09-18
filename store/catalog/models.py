from django.contrib.auth.models import User
from django.db import models


class ActivedManager(models.Manager):
    """
    Менеджер который выводит только активные (active=True) записи
    """

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Category(models.Model):
    """
    Модель категории товаров
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продуктов
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='products'
    )
    user_actions = models.ManyToManyField(User, through='ProductUserRelation')

    objects = models.Manager()
    actived = ActivedManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductUserRelation(models.Model):
    """
    Модель создающая отошения между продуктами и пользователем.
    Нужна для создания системы лайков, добавления товаров в список желаний и оценки
    """

    RATE_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_wishlist = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f"User: {self.user.username}, product: {self.product.name}"
