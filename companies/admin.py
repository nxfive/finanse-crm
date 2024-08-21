from django.contrib import admin

from .models import Company


class AdminCompany(admin.ModelAdmin):
    list_display = ("name", "slug", "path", "website")


admin.site.register(Company, AdminCompany)
