from django import forms
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
        self.fields["manager"].queryset = Manager.objects.filter(team__isnull=True)
