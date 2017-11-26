from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404

from liqpay import LiqPay
from shop import settings
from .models import Order
from .cart import Cart


class PayView(TemplateView):
    template_name = 'payments/pay.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        cart = Cart(request)
        total_price = cart.get_total_price()
        order_id = request.session['cart']['order_id']
        params = {
            'action': 'pay',
            'amount': str(total_price),
            'currency': 'UAH',
            'description': 'Order Detail',
            'order_id': str(order_id),
            'version': '3',
            'sandbox': 1,  # sandbox mode, set to 1 to enable it
            'server_url': 'http://9b00e5d9.ngrok.io/payment/pay-callback/',  # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            order = get_object_or_404(Order, pk=int(response['order_id']))
            order.paid = True
            order.save()

            print('callback data', response)

        HttpResponse()
