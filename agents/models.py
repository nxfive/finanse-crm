from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Account


class Agent(models.Model):
    class Roles(models.TextChoices):
        NONE = "", _("Select Role")
        SALES = "Sales Agent", _("Sales Agent")
        SUPPORT = "Sales Support Agent", _("Sales Suport Agent")
    
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    birth_date = models.DateField()
    role = models.CharField(max_length=30, choices=Roles.choices)

    class Meta:
        ordering = ("user__last_name", "user__first_name", )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"