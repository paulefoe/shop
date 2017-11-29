from decimal import Decimal
import copy

from .models import Order
from showcase.models import Product
from django.shortcuts import get_object_or_404


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            print('why am i here?')
            print(self.session.get('cart'))
            order = Order()
            order.save()
            cart = self.session['cart'] = {'order_id': order.id}
        self.cart = cart
        self.order = Order.objects.get(pk=int(cart['order_id']))

    def add(self, product_id, colors, sizes, quantity=1):
        product = get_object_or_404(Product, pk=int(product_id))
        product.order = self.order
        if product_id not in self.cart:
            color, size = colors.get(), sizes.get()
            print(color, size, '===================color size')
            self.cart[product_id] = {'name': product.name, 'colors': color.color, 'sizes': size.size,
                                     'quantity': quantity, 'price': str(product.price)}
        self.save()

    def update(self, product_id, colors=None, sizes=None, quantity=None):
        if colors:
            color = colors.get()
            self.cart[product_id]['colors'] = color.color
        if sizes:
            size = sizes.get()
            self.cart[product_id]['sizes'] = size.size
        if quantity:
            # print(product_id)
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        pr = copy.deepcopy(self.cart)
        del pr['order_id']
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        pr = copy.deepcopy(self.cart)
        del pr['order_id']
        return sum(item['quantity'] for item in pr.values())

    def get_total_price(self):
        pr = copy.deepcopy(self.cart)
        del pr['order_id']
        return sum(Decimal(item['price']) * item['quantity'] for item in pr.values())
