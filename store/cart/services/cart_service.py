from django.core.exceptions import ObjectDoesNotExist
from cart.cart import Cart
from catalog.models import Product


class CartService:

    @staticmethod
    def add_to_cart(request, product_id, qty):
        product = Product.actived.get(pk=product_id)
        cart = Cart(request)
        cart.update(product=product, qty=qty)

    @staticmethod
    def update_qty(request, product_id, qty):
        product = Product.actived.get(pk=product_id)
        cart = Cart(request)
        if not cart.is_exist(product):
            raise ObjectDoesNotExist()
        cart.update(product=product, qty=qty)

    @staticmethod
    def delete(request, product_id):
        product = Product.actived.get(pk=product_id)
        cart = Cart(request)
        if not cart.is_exist(product):
            raise ObjectDoesNotExist()
        cart.remove(product)
