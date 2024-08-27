from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import Form

from .models import Company

from leads.forms import CompanyLeadCreateForm
from leads.models import LeadSubmission
from leads.utils import assign_lead_to_team_in_company, assign_lead_to_agent_in_team
from teams.models import Team
from agents.models import Agent


def company_lead_create(
    request: HttpRequest, template_name: str, success_url: str
) -> HttpResponse:
    if request.method == "POST":
        form = CompanyLeadCreateForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.save(path=request.path)

            LeadSubmission.objects.create(
                lead=lead,
                ip_address=request.META.get("REMOTE_ADDR"),
                http_user_agent=request.META.get("HTTP_USER_AGENT"),
            )

            company = lead.company
            if company.leads_assignment == Company.LeadAssignment.AUTO:
                team = assign_lead_to_team_in_company(company, team_type=Team.TeamTypes.SUPPORT)
                if team:
                    lead.team = team
                    agent = assign_lead_to_agent_in_team(team)
                    if agent:
                        lead.agent = agent
            lead.save()
            messages.success(
                request, "Thank you for your message. We will contact you shortly."
            )
            return redirect(success_url)
    else:
        form = CompanyLeadCreateForm()
    return render(request, template_name, {"form": form})


def create_message(operation: str, field_name: str, items: QuerySet) -> str:
    messages = {
        "assign": "successfully assigned to the company.",
        "unassign": "successfully unassigned from the company.",
    }
    return "{} {}".format(
        field_name[:-1].capitalize() if items.count() == 1 else field_name.capitalize(),
        messages[operation],
    )


def check_items_to_unassign(request: HttpRequest, field_name: str, company: Company, redirect_url: str) -> HttpResponseRedirect | None:
    if (field_name == "agents" and not company.agents.exists()) or (field_name == "teams" and not company.teams.exists()):
        messages.info(request, f"The company has no assigned {field_name}.")
        return redirect(redirect_url, company_slug=company.slug)
    

def check_items_to_assign(request: HttpRequest, field_name: str, company: Company, redirect_url: str) -> HttpResponseRedirect | None:
    agents = Agent.objects.filter(team__in=company.teams.all()).exclude(companies__in=[company])
    teams = Team.objects.exclude(pk__in=company.teams.values_list("pk", flat=True))

    if (field_name == "agents" and not agents) or (field_name == "teams" and not teams):
        messages.info(request, f"There are no {field_name} available to assign to this company.")
        return redirect(redirect_url, company_slug=company.slug)
    

def unassign_from_company(
    request: HttpRequest,
    company_slug: str,
    form_class: Form,
    field_name: str,
    template_name: str,
    redirect_url: str,
) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if request.method == "POST":
        form = form_class(request.POST, company=company)
        if form.is_valid():
            items = form.cleaned_data.get(field_name)
            for item in items:
                item.companies.remove(company)

            messages.success(request, create_message("unassign", field_name, items))
            return redirect(redirect_url, company_slug=company_slug)
    else:
        response = check_items_to_unassign(request, field_name, company, redirect_url)
        if response:
            return response

        form = form_class(company=company)

    return render(request, template_name, context={"company": company, "form": form})


def assign_to_company(
    request: HttpRequest,
    company_slug: str,
    form_class: Form,
    field_name: str,
    template_name: str,
    redirect_url: str,
) -> HttpResponse:
    company = get_object_or_404(Company, slug=company_slug)

    if request.method == "POST":
        form = form_class(request.POST, company=company)
        if form.is_valid():
            items = form.cleaned_data.get(field_name)
            for item in items:
                item.companies.add(company)

            messages.success(request, create_message("assign", field_name, items))
            return redirect(redirect_url, company_slug=company_slug)
    else:
        response = check_items_to_assign(request, field_name, company, redirect_url)
        if response:
            return response

        form = form_class(company=company)

    return render(request, template_name, context={"company": company, "form": form})
