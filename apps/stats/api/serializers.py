from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from stats.models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "number", "usd_price", "date"]

