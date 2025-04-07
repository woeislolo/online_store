from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from store.models import Product
from coupons.models import Coupon


class Order(models.Model):
    first_name = models.CharField(max_length=50,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=50,
                                 verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250,
                               verbose_name='Адрес')
    post_code = models.CharField(max_length=6,
                                 verbose_name='Индекс')
    city = models.CharField(max_length=30,
                            verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Время обновления')
    paid = models.BooleanField(default=False,
                               verbose_name='Оплачен')
    stripe_id = models.CharField(max_length=250, 
                                 blank=True,
                                 verbose_name='id платежа в Stripe')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Промокод')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)],
                                   verbose_name='Скидка, %')


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost_before_discount(self):
        """ Возвращает сумму заказа без скидки """
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """ Возвращает сумму скидки """
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)
    
    def get_total_cost(self):
        """ Возвращает сумму заказа с учетом скидки """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    
    def get_stripe_url(self):
        """ Возвращает URL для платежа по заказу на сайте платежного шлюза Stripe """
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,
                              verbose_name='№ заказа')
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE,
                                verbose_name='Товар')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Кол-во')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """ Возвращает стоимость товара в заказе (кол-во товара * цена товара) """
        return self.price * self.quantity
    