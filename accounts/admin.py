from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        "college",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "college",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "college",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "phone",
                "college",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "phone",
                "college",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )