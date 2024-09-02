from django.db import models

from django.db import models
from django.utils.translation import pgettext
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from agents.models import Agent
from accounts.models import Account
from teams.models import Team


class Client(models.Model):

    EMPLOYMENT_TYPES = (
        ("", _("Select Employment Type")),
        (
            "Open-ended Employment Contract",
            pgettext("employment type", "Open-ended Employment Contract"),
        ),  # umowa o prace na czas nieokreslony
        (
            "Fixed-term Employment Contract",
            pgettext("employment type", "Fixed-term Employment Contract"),
        ),  # umowa o prace na czas okreslony
        (
            "Open-ended B2B Contract",
            pgettext("employment type", "Open-ended B2B Contract"),
        ),  # umowa B2B na czas nieokreslony
        (
            "Fixed-term B2B Contract",
            pgettext("employment type", "Fixed-term B2B Contract"),
        ),  # umowa B2B na czas okreslony
        (
            "Contract For Specific Work",
            pgettext("employment type", "Contract For Specific Work"),
        ),  # umowa o dzielo
        (
            "Open-ended Service Agreement",
            pgettext("employment type", "Open-ended Service Agreement"),
        ),  # umowa zlecenie na czas nieokreslony
        (
            "Fixed-term Service Agreement",
            pgettext("employment type", "Fixed-term Service Agreement"),
        ),  # umowa zlecenie na czas okreslony
        (
            "Not Applicable N/A", _("Not Applicable")
        ),
    )
    
    class SourceOfIncome(models.TextChoices):
        NONE = "", _("Select Source Of Income")
        EMPLOYMENT = "Employment", _("Employment")
        BUSINESS = "Business", _("Business")
        INVESTMENT = "Investment", _("Investment")
        RENTAL = "Rental", _("Rental")
        ROYALTIES = "Royalties", _("Royalties")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=25, unique=True)
    birth_date = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    source_of_income = models.CharField(max_length=100, choices=SourceOfIncome.choices)
    employer = models.CharField(max_length=100, null=True, blank=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES, null=True, blank=True)
    employment_start_date = models.DateField(null=True, blank=True)
    employment_end_date = models.DateField(null=True, blank=True)
    liabilities = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    living_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    rate_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creditworthiness = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    processing_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("last_name",)

    def __str__(self):
        return self.first_name + " " + self.phone_number

    def get_age(self):
        current_date = datetime.now().date()
        age = current_date.year - self.birth_date.date().year()

        if current_date.month < self.birth_date.month or (
            current_date.month == self.birth_date.month
            and current_date.day < self.birth_date.day
        ):
            age -= 1

        return age

    def get_net_income(self):
        return self.salary - (self.liabilities + self.rate_per_month)
