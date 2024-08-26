from django.urls import path
from .views import LeadListView, LeadCreateView, LeadUpdateView, LeadDetailView, LeadDeleteView

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="lead-list"),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),

    path("my-leads/", LeadListView.as_view(agent=True), name="my-lead-list"),
    path("my-leads/<int:pk>/", LeadDetailView.as_view(agent=True), name="my-lead-detail"),
    path("my-leads/<int:pk>/update/", LeadUpdateView.as_view(agent=True), name="my-lead-update"),
    path("my-leads/<int:pk>/delete/", LeadDeleteView.as_view(agent=True), name="my-lead-delete"),
]
