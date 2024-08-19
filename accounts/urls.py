from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/<slug:username>/", views.dashboard, name="dashboard"),
    path("login/", views.custom_login, name="login"),
]