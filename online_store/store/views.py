from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *
from .utils import ContextMixin


class ProductListView(ContextMixin, ListView):
    model = Product
    template_name = 'store/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.published.all()
        self.category = 0
        if self.kwargs:
            self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            products = products.filter(category=self.category)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(category=self.category)
        return context | add_context


class ProductDetailView(ContextMixin, DetailView):
    queryset = Product.published.all()
    template_name = 'store/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context()
        return context | add_context