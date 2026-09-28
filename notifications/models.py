from django.conf import settings
from django.db import models


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ("order", "Order"),
        ("payment", "Payment"),
        ("message", "Message"),
        ("product", "Product"),
        ("system", "System"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default="system"
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.title}"