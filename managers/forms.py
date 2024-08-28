from typing import Any

from core.forms import BaseUserForm, Manager


class ManagerForm(BaseUserForm):
    class Meta:
        model = Manager
        fields = BaseUserForm.Meta.fields

    def save(self, commit: bool = True) -> Any:
        manager = super().save(commit=False)
        
        if not manager.pk:
            manager.user.is_manager = True

        if commit:
            manager.user.save() 
            manager.save() 

        return manager
