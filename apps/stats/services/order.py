from datetime import datetime
from typing import List, Set

from django.db import transaction
from django.db.models import QuerySet
from stats.models import Order
from stats.services.ruble_price import get_today_usd_ruble_price
from .utils import convert_date


def get_order_object(order_number: int) -> Order:
    try:
        order = Order.objects.get(number=order_number)
    except Order.DoesNotExist:
        raise ValueError
    return order


@transaction.atomic
def create_order(*, number, usd_price, date) -> Order:
    usd_ruble_price = get_today_usd_ruble_price()

    order = Order(number=number, usd_price=usd_price, date=date)
    order.ruble_price = usd_price * usd_ruble_price
    order.save()

    return order


@transaction.atomic
def update_order(*, order_number, usd_price=None, date=None) -> Order:
    order = get_order_object(order_number)
    update_fields = []

    if usd_price:
        current_usd_ruble_price = get_today_usd_ruble_price()
        ruble_price = usd_price * current_usd_ruble_price

        order.usd_price = usd_price
        order.ruble_price = ruble_price

        update_fields.append(*("usd_price", "ruble_price"))

    if date:
        order.date = date
        update_fields.append("date")

    if len(update_fields) > 0:
        order.save(update_fields=update_fields)

    return order


@transaction.atomic
def delete_order(order_number) -> None:
    order = get_order_object(order_number)
    order.delete()
    return None


@transaction.atomic
def create_orders(orders: List[dict]) -> QuerySet[Order]:
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
    objects = []

    used_ruble_price = get_today_usd_ruble_price()

    for order_dict in orders:
        order = get_order_object(order_dict["order_number"])

        order_dict_usd_amount = order_dict["order_data"]["стоимость,$"]
        order_dict_date = convert_date(
            order_dict["order_data"]["срок поставки"]
        )
        order_new_ruble_price = order_dict_usd_amount * used_ruble_price

        if order.usd_price != order_dict_usd_amount:
            order.usd_price = order_dict_usd_amount
            order.ruble_price = order_new_ruble_price

        if (
            order.usd_price == order_dict_usd_amount
            and order.ruble_price != order_new_ruble_price
        ):
            order.ruble_price = order_new_ruble_price

        if str(order.date) != order_dict_date:
            native_date = order.date
            print(f"Change date {native_date} to {order_dict_date}")
            order.date = order_dict_date

        objects.append(order)

    return Order.objects.bulk_update(
        objects, ["usd_price", "ruble_price", "date"]
    )


@transaction.atomic
def delete_orders(order_numbers: Set[int] | List[int]) -> None:
    print("deleting", order_numbers)
    orders = Order.objects.filter(number__in=order_numbers)
    orders.delete()
    return None
