from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer, WishlistProductsSerializer


class CategoryAPIViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Category 1', description='Some description 1')
        Category.objects.create(name='Category 2', description='Some description 2')
        User.objects.create_superuser(username='admin', password='12345')

    def test_get_request(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        cats = [
            Category.objects.get(pk=1),
            Category.objects.get(pk=2)
        ]
        serialized_data = self._get_serialized_data(cats, many=True)
        self.assertEquals(serialized_data, response.data)

    def test_post_request(self):
        url = reverse('category-list')
        data = {
            'name': 'Category 3',
            'description': 'Some description 3'
        }
        self.client.login(username='admin', password='12345')
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        serialized_data = self._get_serialized_data(
            Category.objects.get(pk=3)
        )
        self.assertEquals(serialized_data, response.data)

        response = self.client.get(url)
        self.assertEquals(3, len(response.data))

    def test_post_request_for_not_logged_in(self):
        url = reverse('category-list')
        data = {
            'name': 'Category 3',
            'description': 'Some description 3'
        }
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_detail_request(self):
        url = reverse('category-detail', args=[1])
        serialized_data = self._get_serialized_data(
            Category.objects.get(pk=1)
        )
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(response.data, serialized_data)

    def test_put_request(self):
        url = reverse('category-detail', args=[1])
        serialized_data = self._get_serialized_data(
            Category.objects.get(pk=1)
        )
        data = {
            'name': 'Category 1 (changed)',
            'description': 'Some more description'
        }
        self.client.login(username='admin', password='12345')
        response = self.client.put(url, data=data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data.get('name') != serialized_data.get('name'))
        self.assertTrue(response.data.get('description') != serialized_data.get('description'))

    def test_delete_request(self):
        url = reverse('category-detail', args=[1])
        self.client.login(username='admin', password='12345')
        response = self.client.delete(url)
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=1)

    def test_delete_request_for_not_logged_in(self):
        url = reverse('category-detail', args=[1])
        response = self.client.delete(url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def _get_serialized_data(self, obj, many=False):
        url = reverse('category-list')
        request = APIRequestFactory().get(url)
        return CategorySerializer(obj, many=many, context={'request': request}).data


class ProductAPIViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Category 1', description='Some description')
        Product.actived.create(name='Product 1', qty=10, price=17.50, category=category)
        Product.actived.create(name='Product 2', qty=25, price=30.99, category=category)
        User.objects.create_superuser(username='admin', password='12345')

    def test_get_request(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        products = [
            Product.objects.get(pk=1),
            Product.objects.get(pk=2)
        ]
        serialized_data = self._get_serialized_data(products, many=True)
        self.assertEquals(serialized_data, response.data.get('results'))
        self.assertTrue(response.data.get('count') == 2)
        self.assertTrue(response.data.get('next') is None)
        self.assertTrue(response.data.get('previous') is None)

    def test_post_request(self):
        url = reverse('product-list')
        data = {
            'name': 'Product 3',
            'qty': 100,
            'price': 99.99,
            'category': Category.objects.get(pk=1)
        }
        self.client.login(username='admin', password='12345')
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        serialized_data = self._get_serialized_data(
            Product.objects.get(pk=3)
        )
        self.assertEquals(serialized_data, response.data)

        response = self.client.get(url)
        self.assertEquals(3, len(response.data.get('results')))

    def test_post_request_for_not_logged_in(self):
        url = reverse('product-list')
        data = {'name': 'Product 3', 'qty': 100, 'price': 99.99}
        response = self.client.post(url, data=data)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_detail_request(self):
        url = reverse('product-detail', args=[1])
        serialized_data = self._get_serialized_data(
            Product.objects.get(pk=1)
        )
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(response.data, serialized_data)

    def test_put_request(self):
        url = reverse('product-detail', args=[1])
        serialized_data = self._get_serialized_data(
            Product.objects.get(pk=1)
        )
        data = {
            'name': 'Product 1 changed',
            'qty': 50,
            'price': 89.99
        }
        self.client.login(username='admin', password='12345')
        response = self.client.put(url, data=data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data.get('name') != serialized_data.get('name'))
        self.assertTrue(response.data.get('qty') != serialized_data.get('qty'))
        self.assertTrue(response.data.get('price') != serialized_data.get('price'))

    def test_delete_request(self):
        url = reverse('product-detail', args=[1])
        self.client.login(username='admin', password='12345')
        response = self.client.delete(url)
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=1)

    def test_delete_request_for_not_logged_in(self):
        url = reverse('product-detail', args=[1])
        response = self.client.delete(url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def _get_serialized_data(self, obj, many=False):
        url = reverse('product-list')
        request = APIRequestFactory().get(url)
        return ProductSerializer(obj, many=many, context={'request': request}).data


class ProductUserRelationAPIViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Product.actived.create(name='Product 1', qty=10, price=17.50)
        Product.actived.create(name='Product 2', qty=50, price=90.50)
        User.objects.create_user(username='testuser1', password='12345')
        User.objects.create_user(username='testuser2', password='12345')

    def test_patch_request_set_like_to_product(self):
        # Checked product before
        product = self._get_product_by_id(pk=1)
        serialized_data = self._get_serialized_data(product)
        self.assertTrue(0 == serialized_data.get('total_likes'))
        # Set Like = True of product
        url = reverse('productuserrelation-detail', args=[1])
        self._user_login(username='testuser1')
        response = self.client.patch(url, data={'like': True})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        # Checked product after
        product = self._get_product_by_id(pk=1)
        serialized_data = self._get_serialized_data(product)
        self.assertTrue(1 == serialized_data.get('total_likes'))

    def test_patch_request_set_rate_to_product(self):
        # Checked product before
        product = self._get_product_by_id(pk=1)
        serialized_data = self._get_serialized_data(product)
        self.assertTrue(serialized_data.get('average_rate') is None)
        # Set rate of product from user1
        url = reverse('productuserrelation-detail', args=[1])
        self._user_login(username='testuser1')
        response = self.client.patch(url, data={'rate': 5})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        # Set rate of product from user2
        url = reverse('productuserrelation-detail', args=[1])
        self._user_login(username='testuser2')
        response = self.client.patch(url, data={'rate': 3})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        # Checked product after
        product = self._get_product_by_id(pk=1)
        serialized_data = self._get_serialized_data(product)
        self.assertTrue('4.00' == serialized_data.get('average_rate'))

    def test_patch_request_set_not_correct_rate(self):
        url = reverse('productuserrelation-detail', args=[1])
        self._user_login(username='testuser1')
        # Set wrong rate '6' to product
        response = self.client.patch(url, data={'rate': 6})
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        error = response.data.get('rate')[0]
        self.assertEquals('invalid_choice', error.code)

    def test_patch_request_for_not_logged_in_user(self):
        url = reverse('productuserrelation-detail', args=[1])
        response = self.client.patch(url, data={'like': True, 'rate': 4})
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_patch_request_add_product_to_wishlist(self):
        self._user_login(username='testuser1')
        # Checked product before
        product = self._get_product_by_id(pk=1)
        self.assertTrue(product.productuserrelation_set.all().first() is None)
        # Added product to wishlist
        response = self.client.patch(reverse('productuserrelation-detail', args=[1]), data={'in_wishlist': True})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        # Checked product after
        product = self._get_product_by_id(pk=1)
        self.assertTrue(product.productuserrelation_set.all().first().in_wishlist is True)

    def test_get_request_wishlist_products_of_user(self):
        self._user_login(username='testuser1')
        # Added products to wishlist
        response = self.client.patch(reverse('productuserrelation-detail', args=[1]), data={'in_wishlist': True})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        response = self.client.patch(reverse('productuserrelation-detail', args=[2]), data={'in_wishlist': True})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        # Checked response data and serialized data
        response = self.client.get(reverse('Product-list'))
        product1 = Product.actived.get(pk=1)
        product2 = Product.actived.get(pk=2)
        request = APIRequestFactory().get(reverse('Product-list'))
        serialized_data = WishlistProductsSerializer([product1, product2], many=True, context={'request': request}).data
        self.assertEquals(serialized_data, response.data)

    def _get_product_by_id(self, pk):
        return Product.actived.filter(pk=pk).annotate(
            total_likes=Count(Case(When(productuserrelation__like=True, then=1))),
            average_rate=Avg('productuserrelation__rate')
        ).first()

    def _get_serialized_data(self, obj, many=False):
        url = reverse('product-list')
        request = APIRequestFactory().get(url)
        return ProductSerializer(obj, many=many, context={'request': request}).data

    def _user_login(self, username):
        self.client.post(
            '/api/v1/auth/token/login/',
            data={'username': username, 'password': '12345'}
        )
        token = Token.objects.get(user__username=username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
