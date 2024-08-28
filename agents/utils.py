from typing import Tuple
from django.forms import Form
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from teams.models import Team
from agents.models import Agent


def check_companies_to_process(
    request: HttpRequest, team: Team, agent: Agent, operation: str
) -> HttpResponseRedirect | None:
    if operation == "assign" and not team.companies.exclude(
        id__in=agent.companies.values_list("id", flat=True)
    ):
        messages.info(
            request, "There are no companies available to assign to this agent."
        )
        return redirect("teams:agents:agent-detail", team.slug, agent.pk)

    if operation == "unassign" and not agent.companies.exists():
        messages.info(
            request, "There are no companies available to unassign from this agent."
        )
        return redirect("teams:agents:agent-detail", team.slug, agent.pk)


def validate_team(request: HttpRequest, team_slug: str) -> bool | HttpResponseRedirect:
    """for agents and manager"""
    team = get_object_or_404(Team, slug=team_slug)

    if not team.is_user_member(request.user):
        messages.error(request, f"You are not a member of the {team.name} team.")
        return redirect("agents:agent-list")

    return True


def validate_team_and_agent(request: HttpRequest, agent_pk: int, team_slug: str=None) -> Tuple[Team, Agent] | HttpResponseRedirect:
    """for admin and managers"""
    if request.user.is_superuser:
        agent = get_object_or_404(Agent, pk=agent_pk)
        if not agent.team:
            messages.error(request, "You cannot assign a company because the agent is not assigned to any team.")
            return redirect("agents:agent-detial", pk=agent_pk)
        return agent.team, agent

    team = get_object_or_404(Team, slug=team_slug)

    if team.manager.user != request.user:
        messages.error(request, "You are not a manager of this team.")
        return redirect("agents:agent-list")

    agent = get_object_or_404(Agent, pk=agent_pk)

    if agent not in team.agents.all():
        messages.error(request, "This agent is not assigned to your team.")
        return redirect("agents:agent-list")
    
    return team, agent


def process_companies(
    request: HttpRequest,
    team_slug: str,
    pk: int,
    form_class: Form,
    operation: str,
    template_name: str,
) -> HttpResponseRedirect:

    result = validate_team_and_agent(request, pk, team_slug)
    if isinstance(result, HttpResponseRedirect):
        return result

    team, agent = result

    if request.method == "POST":
        form = form_class(request.POST, instance=agent, team=team)
        if form.is_valid():
            companies = form.cleaned_data.get("companies")

            operation_func = {
                "assign": agent.companies.add,
                "unassign": agent.companies.remove,
            }.get(operation)

            if operation_func:
                operation_func(*companies)
                messages.success(
                    request, f"Companies successfully {operation}ed."
                )
                return redirect("teams:agents:agent-detail", team_slug=team_slug, pk=pk)
    else:
        form = form_class(instance=agent, team=team)
        response = check_companies_to_process(request, team, agent, operation)
        if response:
            return response

    return render(request, template_name, {"form": form, "agent": agent})
