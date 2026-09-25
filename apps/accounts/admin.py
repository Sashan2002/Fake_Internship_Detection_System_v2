from django.contrib import admin
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Not django.contrib.auth.admin.UserAdmin: that base class assumes a
    # `username` field, which this model deliberately doesn't have
    # (email is USERNAME_FIELD instead).
    list_display = ("id", "email", "name", "role", "is_staff", "created_at")
    search_fields = ("email", "name")
