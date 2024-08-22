from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from managers.models import Manager
from companies.models import Company


class Team(models.Model):
    class TeamTypes(models.TextChoices):
        NONE = "", _("Select Team Type")
        SALES = "Sales", _("Sales")
        SUPPORT = "Sales Support", _("Sales Support")

    name = models.CharField(max_length=50, unique=True)
    team_type = models.CharField(max_length=30, choices=TeamTypes.choices)
    slug = models.SlugField(max_length=20, null=True, blank=True)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name="team")
    companies = models.ManyToManyField(Company, through="TeamCompanyAssignment", related_name="teams_assign")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.team_type}: {self.name}"
    
    def generate_slug(self):
        prefix = "sst" if self.team_type == self.TeamTypes.SUPPORT else "st"
        base_slug = slugify(f"{prefix}-{self.name}")
        slug = base_slug
        num = 1
        while Team.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    @property
    def members(self) -> list:
        members = list(self.agents.all())
        if self.manager:
            members.append(self.manager)
        return members

    @property
    def members_count(self) -> int:
        return len(self.members)
    
    def is_user_member(self, user) -> bool:
        if self.manager and self.manager.user == user:
            return True
        return self.agents.filter(user=user).exists()


class TeamCompanyAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    leads_assignment = models.CharField(max_length=20, choices=Company.LeadAssignment.choices, default=Company.LeadAssignment.AUTO)
