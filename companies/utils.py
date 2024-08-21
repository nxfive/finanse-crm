from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from leads.forms import CompanyLeadCreateForm
from leads.models import LeadSubmission


def company_lead_create(request: HttpRequest, template_name: str, success_url: str) -> HttpResponse:
    if request.method == "POST":
        form = CompanyLeadCreateForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.save(path=request.path)

            LeadSubmission.objects.create(
                lead=lead,
                ip_address=request.META.get("REMOTE_ADDR"),
                http_user_agent=request.META.get("HTTP_USER_AGENT"),
            )

            messages.success(request, "Thank you for your message. We will contact you shortly.")
            return redirect(success_url)
    else:
        form = CompanyLeadCreateForm()
    return render(request, template_name, {"form": form})
