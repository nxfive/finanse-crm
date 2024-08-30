from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import Client
from banks.models import BankProduct


class Sale(models.Model):
    class Status(models.TextChoices):
        NEW = "New", _("New"),
        PENDING = "Pending", ("Pending")
        APPROVED = "Approved", _("Approved")
        REJECTED = "Rejected", _("Rejected")
        MANUAL_CHECK = "Manual Check", _("Manual Check")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sales")
    bank_product = models.ForeignKey(BankProduct, on_delete=models.CASCADE, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_years = models.PositiveIntegerField()  
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f"Sale {self.id} - {self.client} - {self.bank_product}"
