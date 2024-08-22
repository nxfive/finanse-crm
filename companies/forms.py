from django import forms

from .models import Company
from agents.models import Agent


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
            "lead_assignment",
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

    agents = forms.MultipleChoiceField(
        queryset=Agent.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Select Agents",
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company", None)
        self.fields["agents"].choice = self.get_agents_with_teams()

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
