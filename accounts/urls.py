from django.urls import path
from . import views


urlpatterns = [
    path("", views.list_accounts, name="account-list"),
    path("dashboard/<slug:username>/", views.dashboard, name="dashboard"),
    path("login/", views.custom_login, name="login"),
]