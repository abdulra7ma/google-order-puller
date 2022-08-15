import pytest
from stats.models import Order
from stats.selectors import order_object


@pytest.mark.django_db
def test_get_order_selector():
    assert Order.objects.count() == 0

    obj = Order.objects.create(
        number=21343, usd_price=127, ruble_price=127 * 60.8
    )
    assert Order.objects.count() == 1

    order = order_object(obj.number)
    assert order.id == obj.id
    assert order.number == obj.number


@pytest.mark.django_db
def test_get_un_exists_order_selector():
    assert Order.objects.count() == 0

    with pytest.raises(ValueError) as exc_info:
        order_object(21621)

