from typing import Any
from django.contrib import admin
from .forms import AgentCreateForm, AgentUpdateForm
from .models import Agent


class AgentAdmin(admin.ModelAdmin):
    form = AgentUpdateForm
    add_form = AgentCreateForm

    list_display = ("get_user_last_name", "get_user_first_name", "get_user_email", "birth_date", "role",)


    def get_user_last_name(self, obj: Agent) -> str:
        return obj.user.last_name
    
    def get_user_first_name(self, obj: Agent) -> str:
        return obj.user.first_name
    
    def get_user_email(self, obj: Agent) -> str:
        return obj.user.email
    
    get_user_last_name.short_description = "Last Name"
    get_user_first_name.short_description = "First Name"
    get_user_email.short_description = "Email"


    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        if obj is None:
            return self.add_form
        return self.form


admin.site.register(Agent, AgentAdmin)