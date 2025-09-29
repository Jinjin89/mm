"""Serializers for user registration and representation."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user."""

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "full_name", "date_joined")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer used to register new accounts."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "full_name",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone_number"):
            raise serializers.ValidationError(
                {"non_field_errors": [_("Either email or phone number must be supplied.")]}
            )

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": [_("Password confirmation does not match.")]})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password", None)
        return User.objects.create_user(password=password, **validated_data)
