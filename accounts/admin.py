from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Account
from .forms import AccountUpdateForm, AccountCreateForm


class AccountAdmin(BaseUserAdmin):
    form = AccountUpdateForm
    add_form = AccountCreateForm

    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "phone_number",
        "email",
        "last_login",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_superuser", "is_manager")
    list_display_links = (
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = (
        "last_login",
        "date_joined",
        "is_manager",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "birth_date")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "is_manager")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "phone_number",
                    "birth_date",
                    "password",
                    "confirm_password",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("-date_joined",)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
