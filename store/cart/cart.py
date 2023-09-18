from decimal import Decimal
from django.conf import settings
from catalog.models import Product
from coupon.models import Coupon
from coupon.services.coupon_service import CouponService


class Cart:
    """
    Корзина покупок
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get(settings.COUPON_SESSION_ID, None)
        self.coupon = None
        if self.coupon_id:
            self.coupon = CouponService.get_by_id(pk=self.coupon_id)

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def is_exist(self, product):
        """Существует ли продукт в корзине"""
        product_id = str(product.id)
        if product_id in self.cart:
            return True

        return False

    def update(self, product, qty=1):
        """Установка значения кол-ва продуктам в корзине"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': 0, 'price': str(product.price)}

        self.cart[product_id]['qty'] = qty

        self.save()

    def remove(self, product):
        """Удаление продукта из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        """Сохранение корзины"""
        self.session.modified = True

    def get_total_price(self):
        """Возвращается полная стоимость продуктов в корзине"""
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def get_grand_total_price(self):
        """Возвращается полная стоимость продуктов в корзине с учетом скидочного купона"""
        if self.coupon:
            discount_price = self.get_total_price() - self.get_coupon_discount_value()
            if discount_price < 0:
                return Decimal(0)
            else:
                return discount_price.quantize(Decimal('0.00'))

        return self.get_total_price()

    def get_coupon_data(self):
        """Возвращаем данные купона"""
        if self.coupon:
            return {
                'name': self.coupon.coupon,
                'label': self._get_coupon_label(),
                'value': str(self.get_coupon_discount_value()),
            }
        return {}

    def get_coupon_discount_value(self):
        """Вычисляем скидку в зависимости от типа (процентный, фиксированный) купона"""
        if self.coupon:
            if self.coupon.coupon_type == Coupon.TYPE_PERCENT:
                return self._get_percent_discount_value()
            if self.coupon.coupon_type == Coupon.TYPE_FIXED:
                return self._get_fix_discount_value()
        return Decimal(0)

    def _get_coupon_label(self):
        """Метка купона"""
        if self.coupon.coupon_type == Coupon.TYPE_PERCENT:
            return f"-{self.coupon.value}%"
        if self.coupon.coupon_type == Coupon.TYPE_FIXED:
            return f"-{self.coupon.value}"

    def _get_percent_discount_value(self):
        """Вычисление скидки купона на основе процента"""
        result = Decimal((self.get_total_price() / Decimal(100)) * self.coupon.value)
        return result.quantize(Decimal('0.00'))

    def _get_fix_discount_value(self):
        """Возвращается фиксированное значение скидки"""
        return self.coupon.value
