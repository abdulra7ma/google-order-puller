from datetime import date

import pytest
from stats.models import RublePrice
from django.db.utils import IntegrityError

from copy import deepcopy

objects_parameters = {
    "currency_exchange_code": "USD",
    "exchange_date": date.today(),
    "exchange_amount": 60.6,
}


@pytest.mark.django_db
def test_ruble_price_creation_success():
    assert RublePrice.objects.count() == 0

    RublePrice.objects.create(**objects_parameters)

    assert RublePrice.objects.count() == 1
    assert RublePrice.objects.count() > 0


@pytest.mark.django_db
def test_ruble_price_default_exchange_date():
    assert RublePrice.objects.count() == 0

    object_params = deepcopy(objects_parameters)
    del object_params["exchange_date"]

    ruble_price = RublePrice.objects.create(**object_params)

    assert RublePrice.objects.count() == 1
    assert ruble_price.exchange_date == date.today()


@pytest.mark.django_db(transaction=True)
def test_ruble_price_creation_failure():
    assert RublePrice.objects.count() == 0

    with pytest.raises(IntegrityError) as exc_info:
        RublePrice.objects.create()

    assert RublePrice.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_ruble_price_object_delete():
    assert RublePrice.objects.count() == 0

    ruble_price = RublePrice.objects.create(**objects_parameters)
    assert RublePrice.objects.count() == 1

    RublePrice.objects.get(id=ruble_price.id).delete()
    assert RublePrice.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_ruble_price_currency_exchange_code_unique_constraint():
    assert RublePrice.objects.count() == 0

    # создает первый объект в списке объектов
    # и поднять IntegrityError при попытке создать второй объект
    # так как оба имеют одинаковое значение currency_exchange_code
    with pytest.raises(IntegrityError) as exc_info:
        RublePrice.objects.bulk_create(
            [
                RublePrice.objects.create(
                    currency_exchange_code="USD", exchange_amount=55.6
                ),
                RublePrice.objects.create(
                    currency_exchange_code="USD", exchange_amount=55.6
                ),
            ]
        )

    assert RublePrice.objects.count() == 1
