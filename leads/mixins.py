from typing import Any
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.decorators import check_user_team
from leads.models import Lead
from teams.models import Team


class AccessControlMixin:

    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)
        lead = get_object_or_404(Lead, pk=kwargs.get("pk"))

        response = self.handle_access(request, lead, self.team, self.agent)
        if response:
            return response

        return super().dispatch(request, *args, **kwargs)
    
    def handle_access(self, request: HttpRequest, lead: Lead, team: Team, agent: bool) -> HttpResponseRedirect | None:
        if agent:
            if team and (request.user.is_superuser or self.team.manager.user == request.user):
                messages.error(request, "You are not allowed to update this lead.")
                return redirect(reverse('teams:leads:lead-list', kwargs={"team_slug": self.team.slug}))
            
            if request.user.is_superuser and not team:
                messages.error(request, "You are not allowed to update this lead.")
                return redirect(reverse("leads:lead-list"))

        if not request.user.is_superuser:
            if not lead.team or (team and team != lead.team):
                messages.error(request, "You are not allowed to update this lead.")
                return redirect("teams:leads:lead-list", team_slug=team.slug)
            
        if team == lead.team:
            if (lead.agent and lead.agent.user != request.user) or (not request.user.is_manager and not lead.agent):
                messages.error(request, "You are not allowed to update this lead.")
                return redirect("teams:leads:lead-list", team_slug=team.slug)

        return None
