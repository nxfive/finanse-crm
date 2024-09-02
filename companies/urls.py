from django.urls import path
from .views import (
    list_companies,
    CompanyCreateView, 
    CompanyDetailView, 
    CompanyUpdateView, 
    CompanyDeleteView, 
    CompanyLeadsListView, 
    CompanyTeamsListView,
    company_assign_agents,
    company_unassign_agents,
    company_assign_teams,
    company_unassign_teams,
)


app_name = "companies"


urlpatterns = [
    path("", list_companies, name="company-list"),
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("<slug:company_slug>/", CompanyDetailView.as_view(), name="company-detail"),
    path("<slug:company_slug>/update/", CompanyUpdateView.as_view(), name="company-update"),
    path("<slug:company_slug>/delete/", CompanyDeleteView.as_view(), name="company-delete"),
    path("<slug:company_slug>/leads/", CompanyLeadsListView.as_view(), name="company-leads"),
    path("<slug:company_slug>/teams/", CompanyTeamsListView.as_view(), name="company-teams"),
    path("<slug:company_slug>/assign/agents/", company_assign_agents, name="company-agents-assign"),
    path("<slug:company_slug>/assign/teams/", company_assign_teams, name="company-teams-assign"),
    path("<slug:company_slug>/unassign/agents/", company_unassign_agents, name="company-agents-unassign"),
    path("<slug:company_slug>/unassign/teams/", company_unassign_teams, name="company-teams-unassign"),
]