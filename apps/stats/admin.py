# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Order, RublePrice


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'usd_price', 'ruble_price', 'date')
    list_filter = ('date',)


@admin.register(RublePrice)
class RublePriceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'currency_exchange_code',
        'exchange_date',
        'exchange_amount',
    )
    list_filter = ('exchange_date',)