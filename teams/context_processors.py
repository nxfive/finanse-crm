from .models import Team
from agents.models import Agent


def team(request):
    team = None
    if request.user.is_authenticated:
        try:
            team = Team.objects.get(manager__user=request.user)
        except Team.DoesNotExist:
            try:
                agent = Agent.objects.get(user=request.user)
                team = agent.team
            except Agent.DoesNotExist:
                return {}
        except Exception as e:
            return {}
    return {"team": team}


def team_manager(request):
    manager = False
    if request.user.is_authenticated:
        try:
            Team.objects.get(manager__user=request.user)
            manager = True
        except Team.DoesNotExist:
            manager = False
    return {"manager": manager}
