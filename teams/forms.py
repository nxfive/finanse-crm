from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Team
from managers.models import Manager


class TeamForm(forms.ModelForm):
    """
        Form for creating and updating Team model.
    """
    class Meta:
        model = Team
        fields = ("name", "team_type", "manager",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter team name"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["manager"].empty_label = _("Select Manager")

        if self.instance and self.instance.pk:
            self.fields["manager"].initial = self.instance.manager
            self.fields["manager"].queryset = Manager.objects.filter(
                Q(team__isnull=True) | Q(team=self.instance)
            )
        else:
            self.fields["manager"].queryset = Manager.objects.filter(team__isnull=True)

    def clean(self):
        cleaned_data = super().clean()
        team_type = cleaned_data.get("team_type")
        instance = self.instance

        if instance.pk:
            db_team = Team.objects.get(pk=instance.pk)
            if db_team.agents.exists() and db_team.team_type != team_type:
                raise ValidationError("Cannot change 'team type' when team already has agents.")

        return cleaned_data
