from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "buyer",
        "product",
        "quantity",
        "added_at",
        "total_price",
    )

    list_filter = (
        "added_at",
    )

    search_fields = (
        "buyer__email",
        "product__name",
    )

    readonly_fields = (
        "added_at",
        "total_price",
    )

    ordering = (
        "-added_at",
    )