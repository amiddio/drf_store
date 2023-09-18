from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Product, ProductUserRelation
from catalog.serializers import CategorySerializer, ProductSerializer, ProductUserRelationSerializer, \
    WishlistProductsSerializer
from rest_framework.test import APIRequestFactory


class CategorySerializerTestCase(TestCase):

    def test_data_fields(self):
        category = Category.objects.create(name='Category 1', description='Some description 1')
        url = reverse('category-list')
        request = APIRequestFactory().get(url)
        serialized_data = CategorySerializer(category, context={'request': request}).data
        self.assertTrue(1 == serialized_data.get('id'))
        self.assertTrue(serialized_data.get('url').endswith('/categories/1/'))
        self.assertTrue('Category 1' == serialized_data.get('name'))
        self.assertTrue('Some description 1' == serialized_data.get('description'))

class ProductSerializerTestCase(TestCase):

    def test_data_fields(self):
        category = Category.objects.create(name='Category 1', description='Some description 1')
        product = Product.actived.create(name='Product 1', qty=10, price=17.50, category=category)
        url = reverse('product-list')
        request = APIRequestFactory().get(url)
        serialized_data = ProductSerializer(product, context={'request': request}).data
        self.assertTrue(1 == serialized_data.get('id'))
        self.assertTrue('Product 1' == serialized_data.get('name'))
        self.assertTrue(10 == serialized_data.get('qty'))
        self.assertTrue('17.50' == serialized_data.get('price'))
        self.assertTrue(0 == serialized_data.get('total_likes'))
        self.assertTrue(serialized_data.get('average_rate') is None)
        self.assertTrue(serialized_data.get('url').endswith('/products/1/'))
        serialized_data_category = serialized_data.get('category')
        self.assertTrue(1 == serialized_data_category.get('id'))
        self.assertTrue('Category 1' == serialized_data_category.get('name'))
        self.assertTrue(serialized_data_category.get('url').endswith('/categories/1/'))


class ProductUserRelationSerializerTestCase(TestCase):

    def test_data_fields(self):
        user = User.objects.create_user(username='testuser1', password='12345')
        product = Product.actived.create(name='Product 1', qty=10, price=17.50)
        rel = ProductUserRelation.objects.create(
            user=user, product=product, like=True, in_wishlist=True, rate=5
        )
        serializer_data = ProductUserRelationSerializer(rel).data
        expected_data = {'product': 1, 'like': True, 'in_wishlist': True, 'rate': 5}
        self.assertEquals(expected_data, serializer_data)


class WishlistProductsSerializerTestCase(TestCase):

    def test_data_fields(self):
        user = User.objects.create_user(username='testuser1', password='12345')
        product = Product.actived.create(name='Product 1', qty=10, price=17.50)
        ProductUserRelation.objects.create(
            user=user, product=product, like=True, in_wishlist=True, rate=5
        )
        serializer_data = WishlistProductsSerializer(product).data
        expected_data = {'id': 1, 'name': 'Product 1', 'price': '17.50'}
        self.assertEquals(expected_data, serializer_data)
