from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):

    ROLE_CHOICES = (
    ("user", "User"),
    ("admin", "Admin"),
)

    username = None

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    college = models.CharField(
        max_length=150,
        blank=True
    )

    role = models.CharField(
    max_length=10,
    choices=ROLE_CHOICES,
    default="user"
)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []