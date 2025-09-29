"""Custom user model for the music platform."""
from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager that supports email and phone registration."""

    use_in_migrations = True

    def _create_user(self, email: str | None, phone_number: str | None, password: str | None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("Users must have either an email address or phone number")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str | None = None, phone_number: str | None = None, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email: str | None = None, phone_number: str | None = None, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """A minimal custom user model that supports email and phone login."""

    email = models.EmailField("email address", unique=True, null=True, blank=True)
    phone_number = models.CharField("phone number", max_length=32, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        identifier = self.email or self.phone_number or "user"
        return str(identifier)

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            raise models.ValidationError("Either email or phone number must be provided.")
