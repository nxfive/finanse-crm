from django.db import models
from django.utils.translation import gettext_lazy as _


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
    phone_number = models.CharField(max_length=25)
    product = models.CharField(max_length=25, choices=FinancialProducts.choices)
    message = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=15, choices=LeadStatus.choices, default=LeadStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.first_name}: {self.phone_number}"