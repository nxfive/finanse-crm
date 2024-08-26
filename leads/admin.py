from typing import Any
from django.contrib import admin
from .models import Lead
from .forms import LeadAdminForm


class LeadAdmin(admin.ModelAdmin):
    form = LeadAdminForm
    
    list_display = (
        "pk",
        "first_name",
        "phone_number",
        "product",
        "status",
        "team",
        "agent",
        "company",
        "created_at",
    )
    list_display_links = (
        "first_name",
        "phone_number",
    )
    search_fields = ("phone_number",)


admin.site.register(Lead, LeadAdmin)
