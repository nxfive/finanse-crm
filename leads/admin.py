from typing import Any
from django.contrib import admin
from .models import Lead
from .forms import LeadUpdateForm, LeadCreateForm


class LeadAdmin(admin.ModelAdmin):
    form = LeadUpdateForm
    add_form = LeadCreateForm
    list_display = (
        "first_name",
        "phone_number",
        "product",
        "status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "first_name",
        "phone_number",
    )
    search_fields = ("phone_number",)

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        if obj is None:
            return self.add_form
        return self.form


admin.site.register(Lead, LeadAdmin)
