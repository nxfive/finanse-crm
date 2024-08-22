from django.urls import path
from .views import (
    CompanyListView, 
    CompanyCreateView, 
    CompanyDetailView, 
    CompanyUpdateView, 
    CompanyDeleteView, 
    CompanyLeadsListView, 
    CompanyTeamsListView,
    company_assign_agents,

)


app_name = "companies"


urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("<slug:company_slug>/", CompanyDetailView.as_view(), name="company-detail"),
    path("<slug:company_slug>/update/", CompanyUpdateView.as_view(), name="company-update"),
    path("<slug:company_slug>/delete/", CompanyDeleteView.as_view(), name="company-delete"),
    path("<slug:company_slug>/leads/", CompanyLeadsListView.as_view(), name="company-leads"),
    path("<slug:company_slug>/teams/", CompanyTeamsListView.as_view(), name="company-teams"),
    path("<slug:company_slug>/assign/agents/", company_assign_agents, name="company-agents-assign"),

]