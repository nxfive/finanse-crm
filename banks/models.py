from django.db import models
from core.models import Address
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    name = models.CharField(max_length=30, unique=True)
    headquarters = models.CharField(max_length=30)
    customer_service = models.CharField(max_length=15)
    established = models.DateField()
    chairman = models.CharField(max_length=60)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class BankProduct(models.Model):
    class ProductType(models.TextChoices):
        MORTGAGE_LOAN = "Mortgage Loan", _("Mortgage Loan"),
        PERSONAL_LOAN = "Personal Loan", _("Personal Loan"),
        CREDIT_CARD = "Credit Card", _("Credit Card"),
        INVESTMENTS = "Investments", _("Investments")

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=20, choices=ProductType.choices)
    description = models.TextField(blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terms = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_product_type_display()
