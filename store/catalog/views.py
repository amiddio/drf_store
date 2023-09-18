from django.db.models import Count, Case, When, Avg, Prefetch
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from catalog.models import Product, Category, ProductUserRelation
from catalog.serializers import ProductSerializer, CategorySerializer, ProductUserRelationSerializer, \
    WishlistProductsSerializer
from store.paginations import ProductsPagination
from store.permissions import IsStaffOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Представление категорий.
    Для админов существует возможность управлять категориями.
    """

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Представление продуктов.
    Для админов существует возможность управлять товарами.
    """

    queryset = Product.actived.all().annotate(
        total_likes=Count(Case(When(productuserrelation__like=True, then=1))),
        average_rate=Avg('productuserrelation__rate')
    ).order_by('id')
    serializer_class = ProductSerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = ProductsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('name', 'price')


class ProductUserRelationView(UpdateModelMixin, GenericViewSet):
    """
    Представление отношений продуктов и пользователей
    """

    queryset = ProductUserRelation.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductUserRelationSerializer
    lookup_field = 'product_id'

    def get_object(self):
        obj, created = ProductUserRelation.objects.get_or_create(
            user=self.request.user, product_id=self.kwargs['product_id']
        )
        return obj


class WishlistProductsView(ListModelMixin, GenericViewSet):
    """
    Представление продуктов в списке желаний
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistProductsSerializer

    def get_queryset(self):
        products = Product.actived\
            .filter(productuserrelation__user=self.request.user, productuserrelation__in_wishlist=True)\
            .order_by('name')
        return products
