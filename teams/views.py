from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from .models import Team, TeamCompanyAssignment
from .forms import TeamForm
from core.utils import paginate_queryset
from core.mixins import AdminRequiredMixin
from companies.models import Company


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "teams/team_list.html"
    context_object_name = "teams"
    paginate_by = 8

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["teams"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        return context


class TeamCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = TeamForm
    template_name = "teams/team_create.html"
    success_url = reverse_lazy("teams:team-list")


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_detail.html"
    context_object_name = "team"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Team, slug=self.kwargs["team_slug"])
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        if (self.object.manager.user == request.user or request.user.is_superuser or request.user in self.object.members):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have a permission to access this team")
            return redirect("teams:team-list")
    

class TeamDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    # model = Team
    template_name = "teams/team_delete.html"
    # context_object_name = "team"
    success_url = reverse_lazy("teams:team-list")

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Team, slug=self.kwargs["team_slug"])
    
    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Team successfully deleted.")
        return super().delete(request, *args, **kwargs)


class TeamUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = "teams/team_update.html"
    form_class = TeamForm
    context_object_name = "team"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Team, slug=self.kwargs["team_slug"])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(leads_assignment__in=[Company.LeadAssignment.AUTO, Company.LeadAssignment.MANUAL])
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        team = form.save()
        companies = self.request.POST.getlist("companies")

        for company_id in companies:
            leads_assignment = self.request.POST.get(f"leads_assignment_{company_id}")
            if leads_assignment == "auto":
                leads_assignment = Company.LeadAssignment.AUTO
            elif leads_assignment == "manual":
                leads_assignment = Company.LeadAssignment.MANUAL
            elif leads_assignment == "disabled":
                leads_assignment = Company.LeadAssignment.DISABLED

            assignment, _ = TeamCompanyAssignment.objects.get_or_create(
                team=team, company=Company.objects.get(id=company_id)
            )
            assignment.leads_assignment = leads_assignment
            assignment.save()
        messages.success(self.request, "Team successfully updated.")
        return super().form_valid(form)