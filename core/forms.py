from django import forms
from accounts.models import Account
from agents.models import Agent
from managers.models import Manager


class BaseUserForm(forms.ModelForm):
    class Meta:
        fields = ("user",)

    def __init__(self, *args, **kwargs):
        if self.__class__ == BaseUserForm:
            raise NotImplementedError("BaseUserForm cannot be instantiated directly.")
        super().__init__(*args, **kwargs)
        
        admins_id = list(Account.objects.filter(is_superuser=True).values_list("id", flat=True))
        agents_id = list(Agent.objects.values_list("user__id", flat=True))
        managers_id = list(Manager.objects.values_list("user__id", flat=True))

        self.fields["user"].queryset = Account.objects.exclude(pk__in=admins_id + agents_id + managers_id)
        self.fields["user"].empty_label = "Select User"
