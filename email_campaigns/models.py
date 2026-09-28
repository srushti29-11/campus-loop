from django.conf import settings
from django.db import models


class EmailCampaign(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("scheduled", "Scheduled"),
        ("sent", "Sent"),
    )

    AUDIENCE_CHOICES = (
        ("all", "All Users"),
        ("active", "Active Users"),
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="email_campaigns"
    )

    subject = models.CharField(max_length=200)

    message = models.TextField()

    audience = models.CharField(
        max_length=20,
        choices=AUDIENCE_CHOICES,
        default="all"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    recipient_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject