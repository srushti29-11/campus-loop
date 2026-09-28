from django.contrib import admin
from .models import EmailCampaign


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "subject",
        "created_by",
        "audience",
        "status",
        "recipient_count",
        "sent_at",
        "created_at",
    )

    list_filter = (
        "audience",
        "status",
        "created_at",
    )

    search_fields = (
        "subject",
        "message",
        "created_by__email",
    )

    readonly_fields = (
        "recipient_count",
        "sent_at",
        "created_at",
    )

    ordering = (
        "-created_at",
    )