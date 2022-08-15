from datetime import date

import pytest
from stats.models import Order
from django.db.utils import IntegrityError

from copy import deepcopy

objects_parameters = {
    "number": 876,
    "usd_price": 125,
    "ruble_price": 125 * 12,
    "date": date.today(),
}


@pytest.mark.django_db
def test_order_creation_success():
    assert Order.objects.count() == 0

    Order.objects.create(**objects_parameters)

    assert Order.objects.count() == 1
    assert Order.objects.count() > 0


@pytest.mark.django_db
def test_order_default_date():
    assert Order.objects.count() == 0

    object_params = deepcopy(objects_parameters)
    del object_params["date"]

    order = Order.objects.create(**object_params)

    assert Order.objects.count() == 1
    assert order.date == date.today()


@pytest.mark.django_db(transaction=True)
def test_order_object_delete():
    assert Order.objects.count() == 0

    order = Order.objects.create(**objects_parameters)
    assert Order.objects.count() == 1

    Order.objects.get(id=order.id).delete()
    assert Order.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_order_creation_failure():
    assert Order.objects.count() == 0

    with pytest.raises(IntegrityError) as exc_info:
        Order.objects.create()

    assert Order.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_order_number_length():
    """
    Протестируйте возникновение ошибки OverflowError
    когда Order number превышает 9223372036854775807
    """

    assert Order.objects.count() == 0

    object_params = deepcopy(objects_parameters)
    object_params["number"] = 876546789876546786567

    with pytest.raises(OverflowError) as exc_info:
        Order.objects.create(**object_params)

    assert Order.objects.count() == 0
