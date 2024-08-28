from django.contrib import admin

from .forms import ManagerForm
from .models import Manager
from core.admin import BaseUserAdmin


class ManagerAdmin(BaseUserAdmin):
    form = ManagerForm
    list_display = BaseUserAdmin.list_display + (
        "team",
        "get_agents_amount",
    )

    def get_agents_amount(self, obj: Manager) -> int | None:
        if obj:
            return len(obj.team.agents.all())

    get_agents_amount.short_description = "Agents"

    ordering = ("team", "user__last_name")


admin.site.register(Manager, ManagerAdmin)
