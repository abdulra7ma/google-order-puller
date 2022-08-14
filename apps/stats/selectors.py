from datetime import date

from stats.models import Order, RublePrice
from stats.services.ruble_price import (
    create_ruble_price_instance,
    update_ruble_price,
)
from stats.utils.currency import get_usd_ruble_today_exchange


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


def order_object(order_number: int) -> Order:
    """
    Получает объект Order по order_number, если не существует, вызывает ValueError

    Returns:
        -> order (Order)
    """

    try:
        order = Order.objects.get(number=order_number)
    except Order.DoesNotExist:
        raise ValueError
    return order


def ruble_price_object(curreny_code: int) -> RublePrice:
    """
    Получает объект RublePrice по curreny_code, если не существует, вызывает ValueError

    Returns:
        -> ruble_price (RublePrice)
    """

    try:
        ruble_price = RublePrice.objects.get(
            currency_exchange_code=curreny_code
        )
    except RublePrice.DoesNotExist:
        raise ValueError
    return ruble_price
