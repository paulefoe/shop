from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Category, Product
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CategoryListView(ListView):
    model = Category
    # template_name = 'category_list.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        result = []
        context = {}
        if query:
            context['object_list'] = Category.objects.filter(name__icontains=query)
        else:
            context = super(CategoryListView, self).get_context_data(**kwargs)
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = {}
        query = self.request.GET.get('q')
        if query:
            context['objects'] = Product.objects.filter(name__icontains=query)
        else:
            context['objects'] = Product.objects.filter(category=self.get_object().id)
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

