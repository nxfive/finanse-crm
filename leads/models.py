from django.db import models


class Lead(models.Model):
    first_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=25)
    message = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.first_name}: {self.phone_number}"