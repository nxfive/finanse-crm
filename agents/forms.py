from django import forms
from .models import Agent


class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("user", "birth_date", "role",)
        widgets = {
            "birth_date": forms.DateInput(attrs={"type":"date"})
        }


class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("role",)
