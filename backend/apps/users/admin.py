"""Django Admin configuration using Unfold."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from apps.tenants.models import UserTenantRole
from apps.users.models import CustomUser


class UserTenantRoleInline(admin.TabularInline):
    """Inline admin for user tenant roles."""

    model = UserTenantRole
    extra = 0
    readonly_fields = ["created_at", "updated_at"]


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    """Admin configuration for CustomUser model."""

    list_display = [
        "email",
        "is_email_verified",
        "is_active",
        "is_superuser",
        "tenant_roles_count",
        "date_joined",
    ]

    list_filter = [
        "is_email_verified",
        "is_active",
        "is_superuser",
        "date_joined",
    ]

    search_fields = ["email"]

    readonly_fields = [
        "date_joined",
        "last_login",
    ]

    filter_horizontal = []
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Status",
            {"fields": ("is_active", "is_email_verified", "is_superuser")},
        ),
        (
            "Tokens",
            {
                "fields": (
                    "email_verification_token",
                    "email_verification_token_expires",
                    "password_reset_token",
                    "password_reset_token_expires",
                )
            },
        ),
        ("Dates", {"fields": ("date_joined", "last_login")}),
    )

    inlines = [UserTenantRoleInline]

    def tenant_roles_count(self, obj):
        """Display tenant roles count."""
        return obj.tenant_roles.count()

    tenant_roles_count.short_description = "Tenants"
