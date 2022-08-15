import pytest
from stats.models import RublePrice
from stats.selectors import ruble_price_object


@pytest.mark.django_db
def test_get_ruble_price_selector():
    assert RublePrice.objects.count() == 0

    obj = RublePrice.objects.create(
        currency_exchange_code="USD", exchange_amount=55.6
    )
    assert RublePrice.objects.count() == 1

    ruble_price = ruble_price_object(obj.currency_exchange_code)
    assert ruble_price.id == obj.id
    assert float(ruble_price.exchange_amount) == obj.exchange_amount


@pytest.mark.django_db
def test_get_un_exists_ruble_price_selector():
    assert RublePrice.objects.count() == 0

    with pytest.raises(ValueError) as exc_info:
        ruble_price_object("USD")
