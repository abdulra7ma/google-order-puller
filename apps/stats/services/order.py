"""
отвечает за все операции CRUD модели Order
"""

from typing import List, Set

from django.db import transaction
from django.db.models import QuerySet
from stats.models import Order
from stats.selectors import get_today_usd_ruble_price, order_object

from .utils import convert_date


@transaction.atomic
def create_orders(orders: List[dict]) -> QuerySet[Order]:
    """
    Проанализируйте orders list и сохраните проанализированные данные в базе данных.

    Returns:
        -> QuerySet[Order]
    """

    objects = []

    used_ruble_price = get_today_usd_ruble_price()

    for order in orders:
        objects.append(
            Order(
                number=order["заказ №"],
                usd_price=order["стоимость,$"],
                ruble_price=used_ruble_price * order["стоимость,$"],
                date=convert_date(order["срок поставки"]),
            )
        )

    return Order.objects.bulk_create(objects)


@transaction.atomic
def update_orders(orders: List[dict]) -> QuerySet[Order]:
    """
    Проанализируйте данные данных заказов и проверьте, нужно ли обновлять заказ,
    если он добавляет объекты для обновления и обновления.

    Returns:
        -> QuerySet[Order]
    """

    objects = []

    used_ruble_price = get_today_usd_ruble_price()

    for order_dict in orders:
        order = order_object(order_dict["order_number"])

        order_dict_usd_amount = order_dict["order_data"]["стоимость,$"]
        order_dict_date = convert_date(
            order_dict["order_data"]["срок поставки"]
        )
        order_new_ruble_price = order_dict_usd_amount * used_ruble_price

        # если цена ордера в долларах изменилась, то меняет текущее значение
        # и получить актуальный курс обмена доллара на рубль
        # и меняем значение столбца рубли на самое последнее
        if order.usd_price != order_dict_usd_amount:
            order.usd_price = order_dict_usd_amount
            order.ruble_price = order_new_ruble_price

        # если цена ордера в долларах не изменилась, а курс рубля к доллару изменился,
        # он заменяет текущую колонку ruble_price на последнее значение
        if (
            order.usd_price == order_dict_usd_amount
            and order.ruble_price != order_new_ruble_price
        ):
            order.ruble_price = order_new_ruble_price

        if str(order.date) != order_dict_date:
            order.date = order_dict_date

        objects.append(order)

    return Order.objects.bulk_update(
        objects, ["usd_price", "ruble_price", "date"]
    )


@transaction.atomic
def delete_orders(order_numbers: Set[int] | List[int]) -> None:
    """
    Удаляет все заказы, на которые есть ссылка в order_numbers
    """
    orders = Order.objects.filter(number__in=order_numbers)
    orders.delete()
    return None
