from django.contrib import admin

from .models import Company


class AdminCompany(admin.ModelAdmin):
    list_display = ("name", "slug", "path", "website", "leads_assignment")


admin.site.register(Company, AdminCompany)
