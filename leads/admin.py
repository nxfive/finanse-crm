from django.contrib import admin
from .models import Lead, LeadSubmission
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


class LeadSubmissionAdmin(admin.ModelAdmin):
    list_display = ("lead", "ip_address", "http_user_agent", "timestamp",)
    readonly_fields = ("lead", "ip_address", "http_user_agent", "timestamp", "location")


admin.site.register(Lead, LeadAdmin)
admin.site.register(LeadSubmission, LeadSubmissionAdmin)
