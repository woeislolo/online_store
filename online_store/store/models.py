from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)
    

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')
    name = models.CharField(max_length=200,
                            verbose_name='Наименование')
    slug = models.SlugField(max_length=200,
                            verbose_name='Слаг')
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True,
                              verbose_name='Изображение')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    available = models.BooleanField(default=True,
                                    verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Добавлен')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменен')
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])
