from django.contrib import admin

from .forms import ManagerForm
from .models import Manager
from core.admin import BaseUserAdmin


class ManagerAdmin(BaseUserAdmin):
    form = ManagerForm
    list_display = BaseUserAdmin.list_display + (
        "get_team",
        "get_members_amount",
    )

    def get_team(self, obj: Manager) -> str | None:
        if obj:
            return obj.team

    def get_members_amount(self, obj: Manager) -> int | None:
        if obj:
            return obj.team.members_count - 1

    get_team.short_description = "Team"
    get_members_amount.short_description = "Agents"

    ordering = ("team", "user__last_name")


admin.site.register(Manager, ManagerAdmin)
