from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

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

