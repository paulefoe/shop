from django.core.mail import send_mail
from celery import task

from shop.sensitive_settings import EMAIL_HOST_USER
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    payment = 'успешно' if order.paid else 'не успешно'
    subject = 'Заказ номер {}'.format(order.id)
    message = 'Вы сделали заказ, id вашего заказа {}, оплата была была произведена {}'.format(order.id, payment)
    mail_sent = send_mail(subject, message, EMAIL_HOST_USER, [order.email])
    return mail_sent
