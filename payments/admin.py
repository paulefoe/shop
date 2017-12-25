from django.contrib import admin

from .models import Order, OrderItem


class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'paid']


class AdminOrderItem(admin.ModelAdmin):
    list_display = ['color', 'size', 'id', 'order', 'product', 'price', 'quantity']

admin.site.register(Order, AdminOrder)
admin.site.register(OrderItem, AdminOrderItem)
