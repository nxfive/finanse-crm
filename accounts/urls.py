from django.urls import path
from . import views

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("", views.list_accounts, name="account-list"),
    path("dashboard/<slug:username>/", views.dashboard, name="dashboard"),
    path("dashboard/<slug:username>/profile/", views.view_profile, name="profile"),
    path("dashboard/<slug:username>/profile/update/", views.update_profile, name="profile-update"),
    path("login/", views.login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("activation-sent/", views.activation_sent, name="activation-sent"),
    path("activation-complete/", views.activation_complete, name="activation-complete"),
    path("activation-invalid/", views.activation_invalid , name="activation-invalid"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password-reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-change/", views.change_password, name="password-change"),
]