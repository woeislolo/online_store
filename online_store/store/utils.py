from django.core.cache import cache
from django.db.models import Count

from .models import *


class ContextMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.annotate(Count('products'))
            cache.set('categories', categories, 20)
        context['categories'] = categories
        return context
