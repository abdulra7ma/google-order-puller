from datetime import date

from django.db import transaction
from stats.models import RublePrice
from stats.selectors import ruble_price_object


@transaction.atomic
def create_ruble_price_instance(
    *, currency_code, exchange_date, exchange_amount
):
    """
    Create RubliePrice object
    """
    ruble_price = RublePrice(
        currency_exchange_code=currency_code,
        exchange_date=exchange_date,
        exchange_amount=exchange_amount,
    )
    ruble_price.save()
    return ruble_price


@transaction.atomic
def update_ruble_price(*, currency_code, exchange_date, new_amount):
    """
    Update RubliePrice object
    """
    ruble_price = ruble_price_object(currency_code)

    ruble_price.exchange_date = (
        exchange_date if exchange_date is not None else date.today()
    )
    ruble_price.exchange_amount = new_amount

    ruble_price.save(update_fields=["exchange_date", "exchange_amount"])

    return ruble_price
