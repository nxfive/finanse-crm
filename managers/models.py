from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Account

class Manager(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_team(self):
        try:
            return self.team
        except ObjectDoesNotExist:
            return None
