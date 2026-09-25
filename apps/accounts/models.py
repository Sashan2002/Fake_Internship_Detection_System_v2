"""
Custom User model matching the `users` table in Section 5 / Table 2:
user_id (pk), name, email (unique), password_hash (via Django's built-in
hashing - never plaintext), role, created_at.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractUser):
    username = None  # email replaces username as the login field
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20, choices=[("user", "user"), ("admin", "admin")], default="user"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email
