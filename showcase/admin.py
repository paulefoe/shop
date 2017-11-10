from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'order', 'parent')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'name', 'price', 'description')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
