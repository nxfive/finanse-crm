from typing import Any
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Agent
from .forms import (
    AgentCreateForm,
    AgentUpdateForm,
    AgentCompaniesAssignForm,
    AgentCompaniesUnassignForm,
)
from .utils import process_companies, validate_team_and_agent, validate_team
from core.mixins import AdminRequiredMixin
from core.utils import paginate_queryset
from teams.models import Team


class AgentListView(LoginRequiredMixin, ListView):
    model = Agent
    template_name = "agents/agent_list.html"
    context_object_name = "agents"
    paginate_by = 8

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team_slug = self.kwargs.get("team_slug")
        if not request.user.is_superuser and self.team_slug:
            result = validate_team(self.request, self.team_slug)

            if isinstance(result, HttpResponseRedirect):
                return result
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        if self.team_slug:
            return Agent.objects.filter(team__slug=self.team_slug)
        return Agent.objects.all()
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["agents"] = paginate_queryset(
            request=self.request, queryset=self.get_queryset(), pages=self.paginate_by
        )
        return context


class AgentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = AgentCreateForm
    template_name = "agents/agent_create.html"
    success_url = reverse_lazy("agents:agent-list")


class AgentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Agent
    form_class = AgentUpdateForm
    template_name = "agents/agent_update.html"

    def get_success_url(self) -> str:
        return reverse_lazy("agents:agent-detail", kwargs={"pk": self.kwargs["pk"]})


class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.is_manager:
            messages.error(request, "You are not allowed to view details of this agent.")
            return redirect("agents:agent-list")
        
        team_slug = kwargs.get("team_slug")
        pk = kwargs.get("pk")

        if team_slug and pk:
            result = validate_team_and_agent(request, pk, team_slug)

            if isinstance(result, HttpResponseRedirect):
                return result
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "error")
            return redirect("agents:agent-list")


class AgentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Agent
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    success_url = reverse_lazy("agents:agent-list")


def agent_assign_companies(
    request: HttpRequest, pk: int, team_slug: str=None
) -> HttpResponseRedirect:
    if request.user.is_superuser or request.user.is_manager:
        return process_companies(
            request,
            team_slug,
            pk,
            form_class=AgentCompaniesAssignForm,
            operation="assign",
            template_name="agents/agent_assign_company.html",
        )
    raise PermissionDenied("You do not have permission")


def agent_unassign_companies(
    request: HttpRequest, pk: int, team_slug: str=None
) -> HttpResponseRedirect:
    if request.user.is_superuser or request.user.is_manager:
        return process_companies(
            request,
            team_slug,
            pk,
            form_class=AgentCompaniesUnassignForm,
            operation="unassign",
            template_name="agents/agent_unassign_company.html",
        )
    raise PermissionDenied("You do not have permission")
