from django.urls import path, include
from .views import TeamListView, TeamCreateView, TeamUpdateView, TeamDetailView, TeamDeleteView, update_team_companies

app_name = "teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="team-list"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
    path("<slug:team_slug>/", TeamDetailView.as_view(), name="team-detail"),
    path("<slug:team_slug>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("<slug:team_slug>/update-companies/", update_team_companies, name="team-companies-update"),
    path("<slug:team_slug>/delete/", TeamDeleteView.as_view(), name="team-delete"),

    path("<slug:team_slug>/agents/", include("agents.urls", namespace="agents")),
    path("<slug:team_slug>/leads/", include("leads.urls", namespace="leads")),
    path("<slug:team_slug>/companies/", include("companies.urls", namespace="companies"))
]
