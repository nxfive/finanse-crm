from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("leads/", include("leads.urls")),
    path("accounts/", include("accounts.urls")),
    path("agents/", include("agents.urls")),
    path("teams/", include("teams.urls")),
    path("managers/", include("managers.urls")),
    path("site/", include("companies.websites_urls")),
    path("companies/", include("companies.urls")),
]
