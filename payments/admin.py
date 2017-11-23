from django.contrib import admin

from .models import Order


class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'paid', 'count']

admin.site.register(Order, AdminOrder)
