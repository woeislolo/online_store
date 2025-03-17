from django.urls import path

from .views import *


app_name = 'store'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
