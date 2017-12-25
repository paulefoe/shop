import copy

from django.views.generic import TemplateView, CreateView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from liqpay import LiqPay
from shop import settings
from .models import Order, OrderItem
from .cart import Cart
from .forms import CreateOrder
from showcase.models import Product
from .tasks import order_created


class CreateOrderView(CreateView):
    model = Order
    template_name = 'payments/create_order.html'
    fields = ['address', 'email']
    success_url = '/payment/pay/'

    def form_valid(self, form):
        print(self.request.session['cart'], 'forms')
        order = Order()
        order.address = form.cleaned_data['address']
        order.email = form.cleaned_data['email']
        order.save()
        for product_id, values in self.request.session['cart'].items():
            product = get_object_or_404(Product, id=int(product_id))
            o = OrderItem.objects.create(order=order, product=product, price=product.price,
                                         quantity=values['quantity'], color=values['colors'],
                                         size=values['sizes'])
            o.save()

        self.request.session['cart']['order_id'] = order.id
        self.request.session.modified = True

        print(self.request.session['cart'], 'forms2222222')
        return super().form_valid(form)


class PayView(TemplateView):
    template_name = 'payments/pay.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        order_id = self.request.session['cart']['order_id']
        del self.request.session['cart']['order_id']
        self.request.session.modified = True
        cart = Cart(request)
        print(request.session['cart'], 'forms2222222')
        total_price = cart.get_total_price()
        del self.request.session['cart']
        self.request.session.modified = True
        params = {
            'action': 'pay',
            'amount': str(total_price),
            'currency': 'UAH',
            'description': 'Order Detail',
            'order_id': str(order_id),
            'version': '3',
            'sandbox': 1,  # sandbox mode, set to 1 to enable it
            'server_url': 'http://187f0c45.ngrok.io/payment/pay-callback/',  # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data, 'order_id': order_id})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):

    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            print('callback data', response)
            order_id = int(response['order_id'])
            # print(order_id)
            # order = get_object_or_404(Order, order_id)
            # order.paid = True
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            order_created.delay(order_id)
            return redirect('category_list')
        return HttpResponse()
