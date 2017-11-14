from django.contrib import admin

from .models import Category, Product, Color, Size, Image


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'order', 'parent')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')
    search_fields = ('name', 'tags')
    filter_horizontal = ('color', 'size', 'image')


class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Image, ImageAdmin)
