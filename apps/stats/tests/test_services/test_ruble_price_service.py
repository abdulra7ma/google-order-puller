from datetime import date

import pytest
from stats.models import RublePrice
from stats.services.ruble_price import (
    create_ruble_price_instance,
    update_ruble_price,
)


@pytest.mark.django_db
def test_create_ruble_price_service():
    assert RublePrice.objects.count() == 0

    ruble_price = create_ruble_price_instance(
        currency_code="USD",
        exchange_date=date.today(),
        exchange_amount=60.6,
    )

    assert RublePrice.objects.count() == 1
    assert RublePrice.objects.last().id == ruble_price.id
    assert (
        RublePrice.objects.last().currency_exchange_code
        == ruble_price.currency_exchange_code
    )


@pytest.mark.django_db
def test_update_ruble_price_service():
    assert RublePrice.objects.count() == 0

    ruble_price = create_ruble_price_instance(
        currency_code="USD",
        exchange_date=date.today(),
        exchange_amount=60.6,
    )

    assert RublePrice.objects.count() == 1

    updated_ruble_price = update_ruble_price(
        currency_code=ruble_price.currency_exchange_code,
        exchange_date=date.today(),
        new_amount=55.9,
    )

    assert RublePrice.objects.count() == 1
    assert ruble_price.id == updated_ruble_price.id
    assert (
        ruble_price.currency_exchange_code
        == updated_ruble_price.currency_exchange_code
    )
    assert float(updated_ruble_price.exchange_amount) == 55.9
