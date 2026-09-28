from django.conf import settings
from django.db import models

from products.models import Product


class Commission(models.Model):

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="commissions"
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commissions"
    )

    order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00
    )

    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Commission - Order #{self.order.id}"


class Promotion(models.Model):

    PROMOTION_TYPES = (
        ("featured", "Featured Product"),
        ("banner", "Banner Promotion"),
        ("campus", "Campus Promotion"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending", "Pending"),
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="promotions"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="promotions"
    )

    promotion_type = models.CharField(
        max_length=20,
        choices=PROMOTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.seller.email} - {self.promotion_type}"