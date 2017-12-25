from django.conf.urls import url

from .views import PayView, PayCallbackView, CreateOrderView


urlpatterns = [
    url(r'^pay/$', PayView.as_view(), name='pay_view'),
    url(r'^pay-callback/$', PayCallbackView.as_view(), name='pay_callback'),
    url(r'^create_order/', CreateOrderView.as_view(), name='create_order'),
]