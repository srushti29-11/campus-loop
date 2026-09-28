from decimal import Decimal

from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    delivery_address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def create_commissions(self):
        from revenue.models import Commission

        commission_rate = Decimal("5.00")

        for item in self.items.select_related("product__seller"):

            seller = item.product.seller

            item_amount = item.price * item.quantity

            commission_amount = (
                item_amount
                * commission_rate
                / Decimal("100")
            )

            Commission.objects.create(
                order=self,
                seller=seller,
                order_amount=item_amount,
                commission_rate=commission_rate,
                commission_amount=commission_amount,
            )

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.email}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} - Order #{self.order.id}"
    
   