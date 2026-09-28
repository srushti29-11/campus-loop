from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "seller",
        "category",
        "listing_type",
        "price",
        "stock",
        "condition",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "listing_type",
        "condition",
        "category",
    )

    search_fields = (
        "name",
        "seller__email",
        "description",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )