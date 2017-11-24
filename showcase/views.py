from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.db.models import F

from .models import Category, Product
from payments.models import Order
from payments.forms import AddProductToBasket


class CategoryListView(ListView):
    model = Category
    template_name = 'showcase/category_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Category.objects.filter(name__icontains=query)
        else:
            return super(CategoryListView, self).get_queryset()


class ProductsInCategoryDetailView(DetailView):
    """Возвращает все продукты в одной категории"""
    model = Category
    template_name = 'showcase/category_detail.html'

    def get_context_data(self, **kwargs):

        context = super(ProductsInCategoryDetailView, self).get_context_data()
        category = get_object_or_404(Category, slug=self.get_object().slug)
        query = self.request.GET.get('q')
        if query:
            context['products'] = Product.objects.filter(name__icontains=query).filter(category=category)
        else:
            context['products'] = Product.objects.filter(category=category)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'showcase/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        if self.request.method == 'GET':
            context['form'] = AddProductToBasket()
        # print(self.request.session.get('product'))
        return context

    def post(self, request, *args, **kwargs):
        """
        Создаёт в сессиях ключи с id товаров и со значениями номера заказа, цвета, размера и количества такого вида
        {'1': {'order_id': 33, 'count': 3, 'color': 'black', 'size': 's'}, 
        '2': {'order_id': 33, 'count': 6, 'color': 'black', 'size': 's'}}
        """
        form = AddProductToBasket(self.request.POST)
        # self.request.session.flush()
        if form.is_valid():
            cd = form.cleaned_data
            if 'order' not in self.request.session:
                # если пользователь ещё ничего не добавил в корзину, то
                # создать новый заказ в таблице и добавить ключ в сессии
                order = Order()
                order.count = cd['count']
                order.save()
                order_detail = {kwargs['pk']: {'order_id': order.id, 'count': order.count,
                                'color': str(cd['color'].get()), 'size': str(cd['size'].get())}}
                self.request.session['order'] = order_detail
            else:
                # если заказ уже есть в сессии, то проверить есть ли в заказе id товара, который хотят добавить
                order_detail = self.request.session['order']
                if kwargs['pk'] in order_detail.keys():
                    # Если id товара существует в заказе, то обновить количество заказаного товара
                    order = Order.objects.get(pk=int(order_detail[kwargs['pk']]['order_id']))
                    order.count = F('count') + cd['count']
                    order.save()
                    order = Order.objects.get(pk=int(order_detail[kwargs['pk']]['order_id']))
                    order_detail[kwargs['pk']]['count'] = order.count
                    self.request.session['order'][kwargs['pk']]['count'] = order.count
                else:
                    # Если id товара нет в в заказе, то добавить новый ключ
                    order_pk = list(order_detail.keys())[0]
                    order = Order.objects.get(pk=int(order_detail[order_pk]['order_id']))
                    order.count = cd['count']
                    order.save()
                    order_detail[kwargs['pk']] = {'order_id': order.id, 'count': order.count,
                                                  'color': str(cd['color'].get()), 'size': str(cd['size'].get())}
                    self.request.session['order'] = order_detail
            print(self.request.session['order'])

        return redirect('product_detail', pk=int(kwargs['pk']))


def basket(request, name=None):
    description = {}
    amount = 0
    count = 0

    try:
        order_detail = request.session['order']
        for product_id in order_detail:
            product = get_object_or_404(Product, pk=int(product_id))
            if request.method == 'POST':
                count = request.POST['count']
            quantity = int(count) if count else int(order_detail[product_id]['count'])
            # quantity = int(order_detail[product_id]['count'])
            cost = product.price * quantity
            amount += cost
            size = order_detail[product_id]['size']
            color = order_detail[product_id]['color']
            description[product.id] = {'name': product.name, 'price': product.price,
                                       'quantity': quantity, 'cost': cost, 'size': size, 'color': color}
            print(description.values())
    except KeyError:
        description = {}
    return render(request, 'showcase/basket.html', {'description': description, 'amount': amount,})

