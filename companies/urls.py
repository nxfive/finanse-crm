from django.urls import path
from .views import CompanyListView, CompanyCreateView, CompanyDetailView, CompanyUpdateView, CompanyDeleteView

app_name = "companies"

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("<slug:company_slug>/", CompanyDetailView.as_view(), name="company-detail"),
    path("<slug:company_slug>/update/", CompanyUpdateView.as_view(), name="company-update"),
    path("<slug:company_slug>/delete/", CompanyDeleteView.as_view(), name="company-delete"),
]