from datetime import date

from django.db import models


class Order(models.Model):
    number = models.PositiveIntegerField(verbose_name="заказ №", db_index=True)
    usd_price = models.PositiveIntegerField(verbose_name="стоимость($)")
    ruble_price = models.PositiveIntegerField(verbose_name="стоимость(rub)")
    date = models.DateField(verbose_name="срок поставки", default=date.today)


class RublePrice(models.Model):
    currency_exchange_code = models.CharField(
        verbose_name="Exchange Currency Code",
        default="USD",
        max_length=3,
        unique=True,
    )
    exchange_date = models.DateField(
        verbose_name="Exchange Date", default=date.today
    )
    exchange_amount = models.DecimalField(
        verbose_name="Exchange Amount",
        max_digits=16,
        decimal_places=2,
        blank=False,
    )
