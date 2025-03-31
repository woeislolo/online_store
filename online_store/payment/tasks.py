from io import BytesIO

from django.template.loader import get_template
from django.core.mail import EmailMessage

from celery import shared_task

from xhtml2pdf import pisa

from orders.models import Order


@shared_task
def task_send_invoice_when_payment_completed(order_id):
    """
    Отправляет счет в формате pdf на email после успешной оплаты.
    """
    order = Order.objects.get(id=order_id)

    subject = f'Магазин корейских товаров - Счет №{order.id}'
    message = 'Во вложении вы найдете счет на оплаченный заказ.'
    email = EmailMessage(subject,
                         message,
                         'admin@online_store.com',
                         [order.email])

    attach = BytesIO()

    template = get_template('orders/order/pdf.html')
    context = {'order': order}
    html = template.render(context)

    pisa.CreatePDF(
        html.encode("utf-8"),
        attach, 
        encoding="utf-8",
        )

    email.attach(f'order_{order.id}.pdf',
                 attach.getvalue(),
                 'application/pdf')
    email.send()
