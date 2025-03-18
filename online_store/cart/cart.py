from decimal import Decimal

from django.conf import settings

from store.models import Product


class Cart:
    def __init__(self, request):
        """ Инициализирует корзину """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ Итерирует товары в корзине и получает их из БД """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Считает кол-во товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """ Добавляет товар в корзину или обновляет кол-во товара. """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # помечаем сеанс "измененным", чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        """ Удаляет товар из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """ Удаляет корзину из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """ Получает общую сумму товаров в корзине """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    