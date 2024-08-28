from .models import LeadAssignmentTracker


def assign_lead_to_team_in_company(company, team_type): 
    teams = [team for team in company.teams.all() if team.team_type == team_type]

    if not teams:
        return None
    
    next_team = None

    tracker, created = LeadAssignmentTracker.objects.get_or_create(company=company, team_type=team_type)

    if (created and len(teams) > 1) or len(teams) == 1:
        next_team = teams[0]

    elif tracker.current_team:
        last_team_index = teams.index(tracker.current_team)
        next_team_index = (last_team_index + 1) % len(teams)
        next_team = teams[next_team_index]

    tracker.current_team = next_team
    tracker.save()
    return next_team


def assign_lead_to_agent_in_team(team):
    agents = team.agents.all()

    if not agents:
        return None
    
    tracker, _ = LeadAssignmentTracker.objects.get_or_create(current_team=team)

    agents_with_company = [agent for agent in agents if tracker.company in agent.companies.all()]

    if not agents_with_company:
        return None
    
    next_agent = None

    if (tracker.current_agent is None and len(agents_with_company) > 1) or len(agents_with_company) == 1:
        next_agent = agents_with_company[0]

    elif tracker.current_agent:
        last_agent_index = agents_with_company.index(tracker.current_agent)
        next_agent_index = (last_agent_index + 1) % len(agents_with_company)
        next_agent = agents_with_company[next_agent_index]

    tracker.current_agent = next_agent
    tracker.save()
    return next_agent
