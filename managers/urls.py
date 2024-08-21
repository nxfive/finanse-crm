from django.urls import path

from .views import ManagerListView, ManagerCreateView, ManagerDeleteView, ManagerDetailView

app_name = "managers"


urlpatterns = [
    path("", ManagerListView.as_view(), name="manager-list"),
    path("create/", ManagerCreateView.as_view(), name="manager-create"),
    path("<int:pk>/", ManagerDetailView.as_view(), name="manager-detail"),
    path("<int:pk>/delete", ManagerDeleteView.as_view(), name="manager-delete")
]