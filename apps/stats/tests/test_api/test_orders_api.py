import os

import pytest
from django.urls import reverse
from rest_framework import status
from stats.models import Order

ORDERS_ENDPOINT = reverse("orders-api")


@pytest.mark.django_db
def test_get_orders_empty_list(client):
    response = client.get(ORDERS_ENDPOINT)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"] == []
    assert response.data["total"] == None


@pytest.mark.django_db
def test_get_orders_list_success(client):
    # создать объект order для его сериализации и возврата
    Order.objects.create(number=21343, usd_price=127, ruble_price=127 * 60.8)

    response = client.get(ORDERS_ENDPOINT)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 1
    assert response.data["total"] == 127
