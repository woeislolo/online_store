from django.core.mail import send_mail

from celery import shared_task

from .models import Order


@shared_task
def task_send_email_after_order_created(order_id):
    """ Отправляет уведомления по электронной почте при успешном создании заказа. """

    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Уважаемый клиент {order.first_name},\n\n' \
    f'вы успешно оформили заказ. ' \
    f'Номер вашего заказа - {order.id}.'
    mail_sent = send_mail(subject=subject,
                              message=message,
                              from_email='admin@online_store.com',
                              recipient_list=[order.email])
    return mail_sent
