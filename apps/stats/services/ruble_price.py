from datetime import date

from django.db import transaction
from stats.models import RublePrice
from stats.selectors import ruble_price_object
from stats.utils.currency import get_usd_ruble_today_exchange


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


def get_today_usd_ruble_price():
    """
    Получите сегодняшнюю цену обмена доллара США на рубль,
    если нет сделать запрос в ЦБ РФ и создать/обновить объект PriceRuble

    Returns:
        -> newly_requested_price (float)
    """

    rub_instance = RublePrice.objects.filter(
        exchange_date=date.today(), currency_exchange_code="USD"
    )

    if rub_instance.exists():
        return rub_instance.first().exchange_amount

    newly_requested_price = get_usd_ruble_today_exchange()
    if RublePrice.objects.filter(currency_exchange_code="USD").exists():
        update_ruble_price(
            currency_code="USD",
            exchange_date=date.today(),
            new_amount=newly_requested_price,
        )
        return newly_requested_price

    create_ruble_price_instance(
        currency_code="USD",
        exchange_date=date.today(),
        exchange_amount=newly_requested_price,
    )

    return newly_requested_price
