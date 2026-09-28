from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sender",
        "receiver",
        "product",
        "message_preview",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "sender__email",
        "receiver__email",
        "message",
        "product__name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    def message_preview(self, obj):
        return obj.message[:50]

    message_preview.short_description = "Message"