from django.urls import path
from .views import OrdersAPIView

urlpatterns = [path("order/", OrdersAPIView.as_view(), name="orders-api")]
