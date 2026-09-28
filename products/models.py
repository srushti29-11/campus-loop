from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    LISTING_TYPES = (
        ("buy", "Buy"),
        ("rent", "Rent"),
        ("exchange", "Exchange"),
        ("free", "Free"),
    )

    CONDITION_CHOICES = (
        ("new", "New"),
        ("like_new", "Like New"),
        ("good", "Good"),
        ("used", "Used"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("sold", "Sold"),
    )

    name = models.CharField(max_length=200)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="good"
    )

    stock = models.PositiveIntegerField(default=1)

    listing_type = models.CharField(
        max_length=20,
        choices=LISTING_TYPES,
        default="buy"
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name