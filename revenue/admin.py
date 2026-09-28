from django.contrib import admin
from .models import Commission, Promotion


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "seller",
        "order_amount",
        "commission_rate",
        "commission_amount",
        "created_at",
    )

    list_filter = (
        "commission_rate",
        "created_at",
    )

    search_fields = (
        "seller__email",
        "order__buyer__email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "seller",
        "product",
        "promotion_type",
        "amount",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )

    list_filter = (
        "promotion_type",
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "seller__email",
        "product__name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )