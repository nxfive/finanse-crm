from django.contrib import admin

from .forms import TeamForm
from .models import Team
from agents.models import Agent


class AgentInline(admin.TabularInline):
    model = Agent
    readonly_fields = ("role",)
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    form = TeamForm
    inlines = (AgentInline, )
    list_display = ("name", "team_type", "slug", "manager")


admin.site.register(Team, TeamAdmin)
