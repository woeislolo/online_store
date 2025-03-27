from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from .models import *
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import *


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            cart.clear()
            task_send_email_after_order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    """ Отображение в админке деталей заказа (is_staff=True, is_active=True) """

    order = get_object_or_404(Order, id=order_id)
    return render(request=request,
                  template_name='admin/orders/order/detail.html',
                  context={'order': order})
