from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category, Product


class CategoryListView(ListView):
    model = Category
    template_name = 'showcase/category_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Category.objects.filter(name__icontains=query)
        else:
            return super(CategoryListView, self).get_queryset()


    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'showcase/category_detail.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(name__icontains=query)
        else:
            return super(CategoryDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = {}
        context['objects'] = self.get_object().categories.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'showcase/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

