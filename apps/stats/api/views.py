from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from stats.models import Order
from stats.utils.swagger import orders_schema

from .serializers import OrderSerializer


class OrdersAPIView(GenericAPIView):
    """
    Возвращает список сериализованных объектов Order
    и общее количество цен заказов в долларах США.
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Orders response object",
                schema=orders_schema,
            )
        },
    )
    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)

        data = {
            "total": self.get_queryset().aggregate(total=Sum("usd_price"))[
                "total"
            ],
            "data": serializer.data,
        }

        return Response(data=data, status=status.HTTP_200_OK)
