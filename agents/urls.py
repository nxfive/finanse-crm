from django.urls import path

from .views import (
    AgentCreateView, 
    AgentUpdateView, 
    AgentDeleteView, 
    AgentDetailView, 
    AgentListView, 
    agent_assign_companies,
    agent_unassign_companies,
)

app_name = "agents"

urlpatterns = [
    path("", AgentListView.as_view(), name="agent-list"),
    path("create/", AgentCreateView.as_view(), name="agent-create"),
    path("<int:pk>/", AgentDetailView.as_view(), name="agent-detail"),
    path("<int:pk>/update/", AgentUpdateView.as_view(), name="agent-update"),
    path("<int:pk>/delete/", AgentDeleteView.as_view(), name="agent-delete"),
    path("<int:pk>/assign/companies/", agent_assign_companies, name="agent-companies-assign"),
    path("<int:pk>/unassign/companies/", agent_unassign_companies, name="agent-companies-unassign"),
]
