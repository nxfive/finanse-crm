from django.urls import path
from .views import (
    LeadListView, 
    LeadCreateView, 
    LeadUpdateView, 
    LeadDetailView, 
    LeadDeleteView,
    lead_assign_agent,
    lead_assign_team,
    lead_unassign_agent,
    lead_unassign_team,
    )

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="lead-list"),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),
    path("<int:pk>/assign/agent/", lead_assign_agent, name="lead-assign-agent"),
    path("<int:pk>/assign/team/", lead_assign_team, name="lead-assign-team"),
    path("<int:pk>/unassign/agent/", lead_unassign_agent, name="lead-unassign-agent"),
    path("<int:pk>/unassign/team", lead_unassign_team, name="lead-unassign-team"),

    path("my-leads/", LeadListView.as_view(agent=True), name="my-lead-list"),
    path("my-leads/<int:pk>/", LeadDetailView.as_view(agent=True), name="my-lead-detail"),
    path("my-leads/<int:pk>/update/", LeadUpdateView.as_view(agent=True), name="my-lead-update"),
    path("my-leads/<int:pk>/delete/", LeadDeleteView.as_view(agent=True), name="my-lead-delete"),
]
