from typing import Any
from django.db.models.query import QuerySet
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from .forms import LeadAdminForm, LeadCreateManagerForm, LeadUpdateManagerForm, LeadUpdateAgentForm, LeadAssignAgentForm, LeadAssignTeamForm
from .models import Lead
from .mixins import AccessControlMixin
from core.utils import paginate_queryset
from core.decorators import check_user_team


class LeadListView(ListView):
    model = Lead
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    paginate_by = 8
    agent = False

    @method_decorator(login_required)
    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)

        if self.agent:
            if not self.team and request.user.is_superuser:
                return redirect(reverse('leads:lead-list'))
            if self.team and (request.user.is_superuser or self.team.manager.user == request.user):
                return redirect(reverse('teams:leads:lead-list', kwargs={"team_slug": self.team.slug}))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_superuser and not self.team and not self.agent:
            return Lead.objects.all()
        if self.kwargs.get("agent", self.agent):
            return Lead.objects.filter(agent__user=self.request.user, team=self.team)
        if self.team:
            return Lead.objects.filter(team=self.team)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["leads"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        context["is_agent"] = self.agent
        return context
    

class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"

    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)

        if not request.user.is_superuser:
            if self.team and self.team.manager.user != request.user:
                raise PermissionDenied("You do not have permission to access this resource.")
            elif not self.team:
                raise PermissionDenied("You do not have permission to access this resource.")

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self) -> BaseModelForm:
        if self.request.user.is_superuser:
            return LeadAdminForm
        return LeadCreateManagerForm

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()

        if self.request.user.is_manager:
            kwargs["user"] = self.request.user
            kwargs["team"] = self.team
        return kwargs
    
    def get_success_url(self) -> str:
        if self.request.user.is_superuser:
            return reverse_lazy("leads:lead-list")
        return reverse_lazy("teams:leads:lead-list", kwargs={"team_slug": self.team.slug})


class LeadUpdateView(LoginRequiredMixin, AccessControlMixin, UpdateView):
    model = Lead
    template_name = "leads/lead_update.html"
    agent = False

    def get_success_url(self) -> str:
        return reverse_lazy("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})
    
    def get_form_class(self) -> BaseModelForm:
        if self.request.user.is_superuser:
            return LeadAdminForm
        elif self.request.user.is_manager:
            return LeadUpdateManagerForm
        return LeadUpdateAgentForm


class LeadDetailView(LoginRequiredMixin, AccessControlMixin, DetailView):
    model = Lead
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    agent = False


class LeadDeleteView(LoginRequiredMixin, AccessControlMixin, DeleteView):
    model = Lead
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead-list")
    agent = False


@login_required
def lead_assign_team(request: HttpRequest, pk: int) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_superuser:
        messages.error(request, "You are not allowed to assign the team.")
        return redirect("teams:leads:lead-list")
    
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = LeadAssignTeamForm(request.POST, lead=lead)
        if form.is_valid():
            team = form.cleaned_data.get("team")
            lead.team = team
            lead.save()
        messages.success(request, "You successfully assign team to the lead.")
        return redirect("leads:lead-detail", pk=pk)
    else:
        if not lead.company.teams.all():
            messages.info(request, "The lead's company has no assigned teams.")
            return redirect("leads:lead-detail", pk=pk)
    
        form = LeadAssignTeamForm(lead=lead)
    return render(request, "leads/lead_assign_team.html", {"form": form, "lead": lead})


@login_required
def lead_assign_agent(request: HttpRequest, pk: int, team_slug: str=None) -> HttpResponse | HttpResponseRedirect:
    lead = get_object_or_404(Lead, pk=pk)

    if not lead.team and request.user.is_superuser:
        messages.error(request, "This lead is not assigned to any team.")
        return redirect("leads:lead-detail", pk=pk)

    if not request.user.is_superuser and lead.team and lead.team.manager.user != request.user:
        messages.error(request, "You are not allowed to assign the agent.")
        return redirect("teams:leads:lead-list")

    if request.method == "POST":
        form = LeadAssignAgentForm(request.POST, lead=lead)
        if form.is_valid():
            agent = form.cleaned_data.get("agent")
            lead.agent = agent
            lead.save()
        messages.success(request, "You successfully assign agent to the lead.")
        if request.user.is_superuser:
            return redirect("leads:lead-detail", pk=pk)
        return redirect("teams:leads:lead-detail", team_slug=team_slug, pk=pk)
    else:
        agents_assigned_to_company = [agent for agent in lead.team.agents.all() if lead.company in agent.companies.all()]

        if not agents_assigned_to_company:
            messages.info(request, "None of the agents on the lead's team are assigned to the lead's company.")
            if request.user.is_superuser:
                return redirect("leads:lead-detail", pk=pk)
            return redirect("teams:leads:lead-detail", team_slug=team_slug, pk=pk)
        
        form = LeadAssignAgentForm(lead=lead)
    return render(request, "leads/lead_assign_agent.html", {"form": form, "lead": lead})


@login_required
def lead_unassign_team(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    if not request.user.is_superuser:
        messages.error(request, "You are not allowed to unassign the team.")
        return redirect("teams:leads:lead-list")
    
    lead = get_object_or_404(Lead, pk=pk)

    lead.team = None
    lead.agent = None
    lead.save()

    return redirect("leads:lead-detail", pk=pk)


@login_required
def lead_unassign_agent(request: HttpRequest, pk: int, team_slug: str=None) -> HttpResponseRedirect:
    lead = get_object_or_404(Lead, pk=pk)
    
    if not request.user.is_superuser or not lead.team or (lead.team and lead.team.manager.user != request.user):
        messages.error(request, "You are not allowed to assign the team.")
        return redirect("teams:leads:lead-list")

    lead.agent = None
    lead.save()

    if request.user.is_superuser:
        return redirect("leads:lead-detail", pk=pk)
    return redirect("teams:leads:lead-detail", team_slug=team_slug, pk=pk)
