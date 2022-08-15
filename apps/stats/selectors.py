from datetime import date

from stats.models import Order, RublePrice


def order_object(order_number: int) -> Order:
    """
    Получает объект Order по order_number, если не существует, вызывает ValueError

    Returns:
        -> order (Order)
    """

    order = Order.objects.filter(number=order_number)

    if order.exists():
        return order.first()
        
    raise ValueError


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
