from django.db import models
from django.utils.translation import gettext_lazy as _

from agents.models import Agent
from teams.models import Team
from companies.models import Company
from core.validators import validate_name, validate_phone_number, validate_team_agent


class Lead(models.Model):
    class FinancialProducts(models.TextChoices):
        NONE = "", _("Select Product")
        CREDIT_CARD = "CC", _("Credit Card")
        INVESTMENTS = "INV", _("Investments")
        DEPOSITS = "DEP", _("Deposits")
        CURRENCY = "CUR", _("Currency")
        LOAN = "LO", _("Loan")

        def __str__(self):
            return f"{self.get_product_display()}"
        
    class LeadStatus(models.TextChoices):
        NEW = "New", _("New")
        CONTACTED = "Contacted", _("Contacted")
        FOLLOW_UP = "Follow-up", _("Follow_up")
        CLOSED = "Closed", _("Closed")

    first_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15)
    product = models.CharField(max_length=25, choices=FinancialProducts.choices)
    message = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=15, choices=LeadStatus.choices, default=LeadStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500)
    email = models.EmailField(unique=True, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.first_name}: {self.phone_number}"

    def clean(self) -> None:
        validate_name(self.first_name)
        validate_phone_number(self.phone_number)
        validate_team_agent(self.team, self.agent)
        return super().clean()

    def save(self, *args, **kwargs):
        path = kwargs.pop("path", None)
        if path:
            try: 
                self.company = Company.objects.get(path=path)
            except Company.DoesNotExist:
                self.company = Company.objects.get(name="Test")
        else:
            self.company = Company.objects.get(name="Test")
        super().save(*args, **kwargs)


class LeadSubmission(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name="submissions")
    ip_address = models.GenericIPAddressField()
    http_user_agent = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
