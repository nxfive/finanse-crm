from django.urls import path
from .views import ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView


app_name = "clients"


urlpatterns = [
    path("", ClientListView.as_view(), name="client-list"),
    path("<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("<int:pk>/update/", ClientUpdateView.as_view(), name="client-update"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client-delete"),

    path("my-clients/", ClientListView.as_view(only_agent=True), name="my-clients"),
    path("my-clients/<int:pk>/", ClientDetailView.as_view(only_agent=True), name="my-client-detail"),
    path("my-clients/<int:pk>/update", ClientUpdateView.as_view(only_agent=True), name="my-client-update"),
]
