from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *
from .utils import ContextMixin, get_user_context
from cart.forms import *


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
        context['category'] = self.category
        add_context = self.get_user_context()
        return context | add_context


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    context = get_user_context()
    context['product'] = product
    context['cart_product_form'] = cart_product_form
    return render(request=request,
                  template_name='store/product/detail.html',
                  context=context)
