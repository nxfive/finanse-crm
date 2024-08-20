from django.urls import path
from .views import TeamListView, TeamCreateView, TeamDetailView, TeamDeleteView

app_name = "teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="team-list"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
    path("<slug:team_slug>/", TeamDetailView.as_view(), name="team-detail"),
    path("<slug:team_slug>/delete", TeamDeleteView.as_view(), name="team-delete"),
]
