from typing import Any
from django import forms

from .models import Lead
from agents.models import Agent
from core.validators import validate_phone_number, validate_name, validate_team_agent


class LeadBaseForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("first_name", "phone_number", "message", "product", "description", "email", "team", "agent",)
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Enter lead name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter lead phone number"}),
            "message": forms.Textarea(attrs={"placeholder": "Enter lead message"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter more information about the lead"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter lead email"})
        }

    def __init__(self, *args, **kwargs):
        if self.__class__ == LeadBaseForm:
            raise NotImplementedError("BaseUserForm cannot be instantiated directly.")
        super().__init__(*args, **kwargs)
        self.fields["team"].empty_label = "Select Team"
        self.fields["agent"].empty_label = "Select Agent"


    def clean_first_name(self) -> dict[str, Any]:
        name = self.cleaned_data.get("first_name")
        validate_name(name)
        return name

    def clean_phone_number(self) -> dict[str, Any]:
        phone = self.cleaned_data.get("phone_number")
        validate_phone_number(phone)
        return phone
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        validate_team_agent(cleaned_data.get("team"), cleaned_data.get("agent"))


class LeadAdminForm(LeadBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["agent"].queryset = Agent.objects.select_related("team").exclude(team__isnull=True)
        self.fields["agent"].label_from_instance = self.agent_label

    def agent_label(self, agent):
        return f"{agent.team.name}: {agent}"
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        validate_team_agent(cleaned_data.get("team"), cleaned_data.get("agent"))


class LeadCreateManagerForm(LeadBaseForm):
    class Meta(LeadBaseForm.Meta):
        exclude = ("description", "email", )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.team = kwargs.pop("team", None)

        super().__init__(*args, **kwargs)
        self.fields["team"].initial = self.team
        self.fields["team"].widget.attrs["readonly"] = True
        self.fields["team"].widget.attrs["disabled"] = True
        
        self.fields["agent"].queryset = Agent.objects.select_related("team").filter(team__manager__user=self.user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.team = self.team

        if commit:
            instance.save()

        return instance


class LeadUpdateManagerForm(LeadBaseForm):
    class Meta(LeadBaseForm.Meta):
        exclude = ("team", "agent",)


class LeadUpdateAgentForm(LeadBaseForm):
    class Meta(LeadBaseForm.Meta):
        exclude = ("phone_number", "message", "team", "agent",)


class CompanyLeadCreateForm(forms.ModelForm):
    """
        This form is intended for users of the company's website."
    """
    class Meta:
        model = Lead
        fields = ("first_name", "phone_number", "product", "message",)
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "message": forms.Textarea(attrs={"placeholder": "Enter your message"}),
        }
