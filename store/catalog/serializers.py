from rest_framework import serializers
from catalog.models import Product, Category, ProductUserRelation


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер категории продуктов
    """

    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер продуктов
    """

    class _InnerCategorySerializer(CategorySerializer):
        class Meta:
            model = Category
            exclude = ('description',)

    category = _InnerCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all())
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='product-detail')
    total_likes = serializers.IntegerField(read_only=True, default=0)
    average_rate = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True, default=None)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'qty', 'price', 'url',
                  'category', 'category_id', 'total_likes', 'average_rate')


class ProductUserRelationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер отношений продуктов и пользователей
    """

    class Meta:
        model = ProductUserRelation
        fields = ('product', 'like', 'in_wishlist', 'rate')


class WishlistProductsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер продуктов в списке желаний
    """

    class Meta:
        model = Product
        fields = ('id', 'name', 'price')
