from django.conf import settings
from django.db import models


class Payment(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    PAYMENT_METHODS = (
        ("test_card", "Test Card"),
        ("upi", "UPI Test"),
        ("cod", "Cash on Delivery"),
    )

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="test_card"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
