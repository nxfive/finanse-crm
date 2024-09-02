from typing import Any, Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django_ratelimit.decorators import ratelimit
from .utils import company_lead_create, unassign_from_company, assign_to_company
from .models import Company
from .forms import (
    CompanyForm,
    CompanyAssignAgentsForm,
    CompanyUnassignAgentsForm,
    CompanyAssignTeamsForm,
    CompanyUnassignTeamsForm,
)
from teams.models import Team
from leads.models import Lead
from core.utils import paginate_queryset
from core.mixins import AdminRequiredMixin
from core.decorators import check_user_team


@ratelimit(key="ip", rate="5/d", method="POST", block=True)
def bank_finanse_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(
        request=request,
        template_name="websites/bank_finanse.html",
        success_url="websites:bank-finanse-sent",
    )


def bank_finanse_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/bank_finanse_sent.html")


@ratelimit(key="ip", rate="5/d", method="POST", block=True)
def house_finder_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(
        request=request,
        template_name="websites/house_finder.html",
        success_url="websites:house-finder-sent",
    )


def house_finder_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/house_finder_sent.html")


@login_required
@check_user_team
def list_companies(request: HttpRequest, team_slug: Optional[str] = None, **kwargs) -> HttpResponse:
    team = kwargs.pop("team", None)

    if not request.user.is_superuser and not team:
        raise Http404

    if request.user.is_superuser:
        queryset = Company.objects.all()
    elif team:
        queryset = team.companies.all()
    else:
        queryset = None
    
    return render(request, "companies/company_list.html", {"companies": paginate_queryset(request, queryset, 8), "user_team": team})
    

@login_required
def get_company(request: HttpRequest, company_slug: str, team_slug: Optional[str] = None) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)
    team = get_object_or_404(Team, slug=team_slug) if team_slug else None

    if not request.user.is_superuser and not team or team and team.manager.user != request.user:
        raise Http404

    return render(request, "companies/company_detail.html", {"company": company})


@login_required
def create_company(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return redirect("companies:company-detail", company_slug=company.slug)
    else:
        form = CompanyForm()

    return render(request, "companies/company_create.html", {"form": form})


class CompanyUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = "companies/company_update.html"
    context_object_name = "company"
    form_class = CompanyForm

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Company, slug=self.kwargs.get("company_slug"))

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request, "Company does not exist.")
            return redirect("companies:company-list")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "companies:company-detail",
            kwargs={"company_slug": self.kwargs["company_slug"]},
        )


class CompanyDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    template_name = "companies/company_delete.html"
    success_url = reverse_lazy("companies:company-list")
    context_object_name = "company"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Company, slug=self.kwargs.get("company_slug"))

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request, "Company does not exist.")
            return redirect("companies:company-list")
        return super().dispatch(request, *args, **kwargs)


class CompanyTeamsListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "companies/company_teams_list.html"
    context_object_name = "teams"
    paginate_by = 8

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = get_object_or_404(Company, slug=kwargs.get("company_slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return self.object.teams.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["company"] = self.object
        context["teams"] = paginate_queryset(
            request=self.request, queryset=self.get_queryset(), pages=self.paginate_by
        )
        return context


class CompanyLeadsListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "companies/company_leads_list.html"
    context_object_name = "leads"
    slug_field = "slug"
    slug_url_kwarg = "company_slug"
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Any]:
        return Lead.objects.filter(company__slug=self.kwargs["company_slug"]).all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["company"] = Company.objects.get(slug=self.kwargs["company_slug"])
        context["leads"] = paginate_queryset(
            request=self.request, queryset=self.get_queryset(), pages=self.paginate_by
        )
        return context


@login_required
def company_assign_agents(
    request: HttpRequest, company_slug: str, team_slug: Optional[str] = None
) -> HttpResponse:
    if request.user.is_superuser:
        return assign_to_company(
            request,
            company_slug,
            form_class=CompanyAssignAgentsForm,
            field_name="agents",
            template_name="companies/company_assign_agent.html",
            redirect_url="companies:company-detail",
        )
    raise PermissionDenied("You do not have permission to access this page.")


@login_required
def company_assign_teams(
    request: HttpRequest, company_slug: str, team_slug: Optional[str] = None
) -> HttpResponse:
    if request.user.is_superuser:
        return assign_to_company(
            request,
            company_slug,
            form_class=CompanyAssignTeamsForm,
            field_name="teams",
            template_name="companies/company_assign_team.html",
            redirect_url="companies:company-detail",
        )
    raise PermissionDenied("You do not have permission to access this page.")


@login_required
def company_unassign_teams(
    request: HttpRequest, company_slug: str, team_slug: Optional[str] = None
) -> HttpResponse:
    if request.user.is_superuser:
        return unassign_from_company(
            request,
            company_slug,
            form_class=CompanyUnassignTeamsForm,
            field_name="teams",
            template_name="companies/company_unassign_team.html",
            redirect_url="companies:company-detail",
        )
    raise PermissionDenied("You do not have permission to access this page.")


@login_required
def company_unassign_agents(
    request: HttpRequest, company_slug: str, team_slug: Optional[str] = None
) -> HttpResponse:
    if request.user.is_superuser:
        return unassign_from_company(
            request,
            company_slug,
            form_class=CompanyUnassignAgentsForm,
            field_name="agents",
            template_name="companies/company_unassign_agent.html",
            redirect_url="companies:company-detail",
        )
    raise PermissionDenied("You do not have permission to access this page.")
