from django.urls import path

from .views import (
    product_list,
    product_detail,
    add_product,
)


urlpatterns = [
    path(
        "",
        product_list,
        name="products",
    ),

    path(
        "<int:product_id>/",
        product_detail,
        name="product_detail",
    ),

    path(
        "add/",
        add_product,
        name="add_product",
    ),
]