from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from .models import *
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import *


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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


@staff_member_required
def admin_order_pdf(request, order_id):
    """ Генерирование счета-фактуры в формате PDF """

    order = get_object_or_404(Order, id=order_id)
    pdfname = f'order_{order.id}.pdf'

    file_object = HttpResponse(content_type='application/pdf')
    file_object['Content-Disposition'] = f'attachment; filename={pdfname}'

    context = {'order': order}
    template = get_template('orders/order/pdf.html')

    html = template.render(context)

    pisa.CreatePDF(
        html.encode("utf-8"),
        file_object, 
        encoding="utf-8",
                   )

    return file_object
