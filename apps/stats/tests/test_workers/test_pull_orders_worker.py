import pytest
from stats.models import Order, RublePrice
from stats.workers.pull_orders import puller_initiator


@pytest.mark.django_db
def test_puller_initiator():
    assert Order.objects.count() == 0
    assert RublePrice.objects.count() == 0

    puller_initiator()

    assert Order.objects.count() > 1
    assert RublePrice.objects.count() == 1
