from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "buyer",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "buyer__email",
        "buyer__first_name",
        "buyer__last_name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = (
        OrderItemInline,
    )

    ordering = (
        "-created_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "product__name",
        "order__buyer__email",
    )