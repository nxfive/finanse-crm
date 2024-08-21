from django  import forms

from core.forms import BaseUserForm, Manager


class ManagerForm(BaseUserForm):
    class Meta:
        model = Manager
        fields = BaseUserForm.Meta.fields
