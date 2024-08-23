from typing import Any
from django.contrib import admin
from .forms import AgentCreateForm, AgentUpdateForm
from .models import Agent
from core.admin import BaseUserAdmin


class AgentAdmin(BaseUserAdmin):
    form = AgentUpdateForm
    add_form = AgentCreateForm

    list_display = BaseUserAdmin.list_display + (
        "role",
        "team",
    )

    ordering = ("team", "role", "user__last_name",)

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        if obj is None:
            return self.add_form
        return self.form


admin.site.register(Agent, AgentAdmin)
