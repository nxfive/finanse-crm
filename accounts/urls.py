from django.urls import path
from . import views


urlpatterns = [
    path("", views.list_accounts, name="account-list"),
    path("dashboard/<slug:username>/", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("activation-sent/", views.activation_sent, name="activation-sent"),
    path("activation-complete/", views.activation_complete, name="activation-complete"),
    path("activation-invalid/", views.activation_invalid , name="activation-invalid"),
]