from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Account
from .forms import AccountUpdateForm, AccountCreateForm


class AccountAdmin(admin.ModelAdmin):
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
    list_filter = ("is_superuser",)
    list_display_links = (
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
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
