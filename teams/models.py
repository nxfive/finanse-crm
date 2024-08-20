from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Team(models.Model):
    class TeamTypes(models.TextChoices):
        NONE = "", _("Select Team Type")
        SALES = "Sales", _("Sales")
        SUPPORT = "Sales Support", _("Sales Support")

    name = models.CharField(max_length=50, unique=True)
    team_type = models.CharField(max_length=30, choices=TeamTypes.choices)
    slug = models.SlugField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.team_type}: {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            prefix = "sst" if self.team_type == self.TeamTypes.SUPPORT else "st"
            base_slug = slugify(f"{prefix}-{self.name}")
            slug = base_slug
            num = 1
            while Team.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

