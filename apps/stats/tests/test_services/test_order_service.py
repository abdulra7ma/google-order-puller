import datetime
from random import randint
from typing import List

import pytest
from django.db.utils import IntegrityError
from stats.models import Order
from stats.services.order import create_orders, update_orders, delete_orders


def prep_orders_data(amount=1):
    data = []

    for _ in range(amount):
        usd_price = randint(750, 1700)

        data.append(
            {
                "заказ №": randint(10000, 99999),
                "стоимость,$": usd_price,
                "срок поставки": datetime.date(
                    randint(2005, 2025), randint(1, 12), randint(1, 28)
                ).strftime("%d.%m.%Y"),
            }
        )

    return data


def prep_update_orders_data(orders_data: List[dict]):
    orders = []

    for order in orders_data:
        orders.append({"order_number": order["заказ №"], "order_data": order})

    return orders


@pytest.mark.django_db
def test_create_orders_service():
    assert Order.objects.count() == 0

    data = prep_orders_data(5)
    create_orders(data)

    assert Order.objects.count() == 5


@pytest.mark.django_db
def test_create_orders_failure_service():
    assert Order.objects.count() == 0

    data = prep_orders_data(5)
    data[0]["заказ №"] = None

    with pytest.raises(IntegrityError) as exc_info:
        create_orders(data)

    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_update_orders_service():
    assert Order.objects.count() == 0

    create_orders_data = prep_orders_data(5)
    create_orders(create_orders_data)

    assert Order.objects.count() == 5

    update_orders_data = prep_update_orders_data(create_orders_data)
    update_orders(update_orders_data)

    assert Order.objects.count() == 5


@pytest.mark.django_db
def test_update_orders_failure_service():
    """
    Обновить несуществующие объекты Order
    """

    assert Order.objects.count() == 0

    create_orders_data = prep_orders_data(5)
    update_orders_data = prep_update_orders_data(create_orders_data)

    with pytest.raises(ValueError) as exc_info:
        update_orders(update_orders_data)

    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_delete_orders_service():
    assert Order.objects.count() == 0

    create_orders_data = prep_orders_data(5)
    create_orders(create_orders_data)

    assert Order.objects.count() == 5

    delete_orders(set(Order.objects.values_list("number", flat=True)))

    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_delete_non_existing_orders_service():
    assert Order.objects.count() == 0

    create_orders_data = prep_orders_data(5)
    delete_orders({order["заказ №"] for order in create_orders_data})
    
    assert Order.objects.count() == 0
