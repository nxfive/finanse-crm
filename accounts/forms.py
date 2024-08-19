from typing import Any
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Account


class AccountCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"
        self.fields["email"].widget.attrs["placeholder"] = "Enter email"

    def clean(self) -> dict[str, Any]:
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError({
                "password": "Passwords do not match"
            })
        return super().clean()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
                                       

class AccountUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ("email", "password", "phone_number", "is_active", "is_staff", "is_superuser",)

