from functools import wraps
from typing import Any, Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from teams.models import Team


def check_user_team(function):
    @wraps(function)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any):
        team_slug = kwargs.pop("team_slug", None)
        
        if request.user.is_superuser and not team_slug:
            return function(request, *args, **kwargs, team=None)
        if team_slug:
            try:
                team = Team.objects.get(slug=team_slug)
                if request.user.is_superuser or any(member.user == request.user for member in team.members):
                    return function(request, *args, **kwargs, team=team)
            except Team.DoesNotExist:
                return redirect(f"/accounts/dashboard/{request.user.username}/")
        return redirect(f"/accounts/dashboard/{request.user.username}/")
    return wrapper
        