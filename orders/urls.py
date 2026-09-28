from django.urls import path

from .views import (
    order_list,
    order_success,
    seller_orders,
    update_seller_order_status,
)


urlpatterns = [

    path(
        "",
        order_list,
        name="orders"
    ),

    path(
        "success/<int:order_id>/",
        order_success,
        name="order_success"
    ),

    path("seller/", seller_orders, name="seller_orders"),

    path(
    "seller/update/<int:order_id>/",
    update_seller_order_status,
    name="update_seller_order_status",
),
]