from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .utils import company_lead_create
from .models import Company
from .forms import CompanyForm
from teams.models import Team
from leads.models import Lead
from core.utils import paginate_queryset
from core.mixins import AdminRequiredMixin
from core.decorators import check_user_team


def bank_finanse_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(request=request, template_name="websites/bank_finanse.html", success_url="websites:bank-finanse-sent")

def bank_finanse_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/bank_finanse_sent.html")

def house_finder_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(request=request, template_name="websites/house_finder.html", success_url="websites:house-finder-sent")

def house_finder_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/house_finder_sent.html")


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "companies/company_list.html"
    context_object_name = "companies"
    slug_field = "slug"
    slug_url_kwarg = "team_slug"
    paginate_by = 8

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = None
        if self.kwargs.get("team_slug"):
            self.team = get_object_or_404(Team, slug=self.kwargs["team_slug"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        if self.team:
            return self.team.companies.all()
        return Company.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.team:
            context["team"] = self.team
        context["companies"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        return context
    

class CompanyCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = "companies/company_create.html"
    form_class = CompanyForm
    success_url = reverse_lazy("companies:company-list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Company successfully created")
        return super().form_valid(form)
    

class CompanyDetailView(LoginRequiredMixin, DetailView):
    template_name = "companies/company_detail.html"
    context_object_name = "company"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Company, slug=self.kwargs.get("company_slug"))

    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request, "Company does not exist.")
            return redirect("companies:company-list")
        return super().dispatch(request, *args, **kwargs)
    

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
        return reverse_lazy("companies:company-detail", kwargs={"company_slug": self.kwargs["company_slug"]})
    

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
        return self.object.teams_assign.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["company"] = self.object
        context["teams"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
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
        context["leads"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        return context
