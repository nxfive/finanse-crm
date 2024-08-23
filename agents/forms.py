from django import forms

from core.forms import BaseUserForm, Agent


class AgentCreateForm(BaseUserForm):
    class Meta:
        model = Agent
        fields = BaseUserForm.Meta.fields + ("birth_date", "role", "team")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type":"date"})
        }


class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("role",)
