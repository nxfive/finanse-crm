from django import forms

from .models import Company
from agents.models import Agent
from teams.models import Team


class CompanyForm(forms.ModelForm):
    """
        Form for create and update Company model.
    """

    class Meta:
        model = Company
        fields = (
            "name",
            "path",
            "website",
            "leads_assignment",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter company name"}),
            "path": forms.TextInput(attrs={"placeholder": "Example: /path/to/source/"}),
            "website": forms.TextInput(attrs={"placeholder": "https://example.com"}),
        }


class CompanyAssignAgentsForm(forms.Form):
    """
        Form for assigning agents to a specific Company.

        This form allows admin users to assign agents to a selected Company.
        The agents available for assignment are filtered based on their team
        association with the Company. Agents whose teams are already linked to
        the Company, but who are not individually assigned yet, will be available
        for selection.
    """

    agents = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Select Agents",
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        self.fields["agents"].choices = self.get_agents_with_teams()

    def get_agents_with_teams(self):
        if self.company:
            agents_team_in_company = Agent.objects.filter(team__companies=self.company)
            agents_not_assign_to_company = agents_team_in_company.exclude(
                companies=self.company
            )
            return [
                (agent.pk, f"{agent.team} - {agent}")
                for agent in agents_not_assign_to_company
            ]
        return []


class CompanyUnassignAgentsForm(forms.Form):
    """
        Form for unassigning agents from a specific Company.

        This form allows admin users to unassign agents from a selected Company.
        The agents available for unassignment are filtered based on their team
        association with the Company. Agents whose teams are already linked to
        the Company and who are individually assigned, will be available
        for unassignment.
    """
    agents = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)
        self.fields["agents"].choices = self.get_agents_with_teams()

    def get_agents_with_teams(self):
        if self.company:
            agents_team_in_company = Agent.objects.filter(team__companies=self.company)
            agents_assign_to_company = agents_team_in_company.filter(companies=self.company)
            return [(agent.pk, f"{agent.team} - {agent}") for agent in agents_assign_to_company]
        return []


class CompanyAssignTeamsForm(forms.Form):
    """
        Form for assigning teams to a specific Company.

        This form allows admin users to assign teams to a selected Company.
    """
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        # label="Select Teams",
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        if self.company:
            assigned_teams_ids = self.company.teams.values_list("id", flat=True)
            self.fields["teams"].queryset = Team.objects.exclude(id__in=assigned_teams_ids)
        else:
            self.fields["teams"].queryset = []


class CompanyUnassignTeamsForm(forms.Form):
    """
        Form for unassigning teams to a specific Company.

        This form allows admin users to unassign teams from a selected Company.
    """
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Select Teams",
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        if self.company:
            assigned_teams_ids = self.company.teams.values_list("id", flat=True)
            self.fields["teams"].queryset = Team.objects.filter(id__in=assigned_teams_ids)
        else:
            self.fields["teams"].queryset = []
