from django import forms
from .models import Agent

from accounts.models import Account

class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("user", "birth_date", "role",)
        widgets = {
            "birth_date": forms.DateInput(attrs={"type":"date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        admins_id = list(Account.objects.filter(is_superuser=True).values_list("id", flat=True))
        agents_id = list(Agent.objects.values_list("user__id", flat=True))

        self.fields["user"].queryset = Account.objects.exclude(pk__in=admins_id + agents_id)


class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("role",)
