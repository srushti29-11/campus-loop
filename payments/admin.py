from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "buyer",
        "amount",
        "payment_method",
        "status",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "buyer__email",
        "buyer__first_name",
        "buyer__last_name",
        "transaction_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )