from typing import Any
from django import forms
from django.core.exceptions import ValidationError

from core.forms import BaseUserForm, Agent
from teams.models import Team
from companies.models import Company


class BaseAgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("role", "team")

    def __init__(self, *args, **kwargs):
        if self.__class__ == BaseUserForm:
            raise NotImplementedError("BaseAgentForm cannot be instantiated directly.")
        super().__init__(*args, **kwargs)

        self.fields["team"].empty_label = "Select Team"

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        team = cleaned_data.get("team")
        if team:
            if role == Agent.Roles.SALES and team.team_type != Team.TeamTypes.SALES:
                raise ValidationError("Sales agent must be assigned to Sales team.")

            if role == Agent.Roles.SUPPORT and team.team_type != Team.TeamTypes.SUPPORT:
                raise ValidationError(
                    "Sales Support agent must be assigned to Sales Support team."
                )


class AgentCreateForm(BaseAgentForm, BaseUserForm):
    class Meta:
        model = BaseAgentForm.Meta.model
        fields = BaseUserForm.Meta.fields + BaseAgentForm.Meta.fields


class AgentUpdateForm(BaseAgentForm):
    class Meta(BaseAgentForm.Meta):
        exclude = ("user",)


class AgentCompaniesAssignForm(forms.ModelForm):
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
        widget=forms.SelectMultiple,
        required=True,
    )
    class Meta:
        model = Agent
        fields = ("companies",)

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team", None)
        super().__init__(*args, **kwargs)

        self.fields["companies"].queryset = self.team.companies.exclude(id__in=self.instance.companies.values_list("id", flat=True))


class AgentCompaniesUnassignForm(forms.ModelForm):
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.none(),
        widget=forms.SelectMultiple,
        required=True,
    )
    class Meta:
        model = Agent
        fields = ("companies",)

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team", None)
        super().__init__(*args, **kwargs)

        self.fields["companies"].queryset = self.instance.companies
