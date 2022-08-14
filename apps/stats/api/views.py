from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from stats.models import Order

from .serializers import OrderSerializer


class OrdersAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().aggregate(total=Sum("usd_price"))[
                "total"
            ],
            "data": serializer.data,
        }

        return Response(data=data, status=status.HTTP_200_OK)
