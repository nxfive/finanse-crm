from functools import wraps
from typing import Any, Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from teams.models import Team


def check_user_team(function: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    @wraps(function)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return function(request, *args, **kwargs, team=None)
    
        team_slug = kwargs.get("team_slug")
        if team_slug:
            try:
                team = Team.objects.get(slug=team_slug)
                if any(member.user == request.user for member in team.members):
                    return function(request, *args, **kwargs, team=team)
            except Team.DoesNotExist:
                return redirect("/")
        return redirect("/")
    return wrapper
        