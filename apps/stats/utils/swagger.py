# external imports
from random import choice

from drf_yasg import openapi

order_properties = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Order System ID",
            example=choice(list(range(0, 9))),
        ),
        "number": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Order Number",
            example=543261521,
        ),
        "usd_price": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Order price in USD",
            example=113,
        ),
        "ruble_price": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Order price in USD",
            example=113,
        ),
        "date": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Order Date",
            example="12.12.2022",
        ),
    },
)

orders_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "total": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Price Total",
            example="50422",
        ),
        "data": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="Order Data",
            items={**order_properties},
        ),
    },
)
