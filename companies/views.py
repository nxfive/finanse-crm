from typing import Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
from core.utils import paginate_queryset
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


@login_required
def update_company(request: HttpRequest, company_slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if not request.user.is_superuser:
        raise Http404
    
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
        return redirect("companies:company-detail", company_slug=company.slug)
    else:
        form = CompanyForm(instance=company)

    return render(request, "companies/company_update.html", {"form": form, "company": company})


@login_required
def delete_company(request: HttpRequest, company_slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if not request.user.is_superuser:
        raise Http404
    
    if request.method == "POST":
        company.delete()
        messages.info(request, "Company successfully deleted")
        return redirect("companies:company-list")

    return render(request, "companies/company_delete.html", {"company": company})


@login_required
def list_company_teams(request: HttpRequest, company_slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if not request.user.is_superuser:
        raise Http404
    
    return render(request, "companies/company_teams_list.html", {"company": company, "teams": paginate_queryset(request, company.teams.all(), 8)})


@login_required
def list_company_leads(request: HttpRequest, company_slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if not request.user.is_superuser:
        raise Http404
    
    return render(request, "companies/company_leads_list.html", {"company": company, "leads": paginate_queryset(request, company.leads.all(), 8)})


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
