from django.db import models

from accounts.models import Account


class Manager(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def delete(self, *args, **kwargs):
        self.user.is_manager = False
        self.user.save()
        
        super().delete(*args, **kwargs)
