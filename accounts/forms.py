from typing import Any
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account, UserProfile
from core.validators import (
    validate_phone_number,
    validate_birth_date,
    validate_passwords,
)


class AccountBaseForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
            "birth_date",
            "password",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "birth_date": forms.DateInput(attrs={"placeholder": "yyyy-mm-dd"}),
        }

    def clean(self) -> dict[str, Any]:
        validate_birth_date(self.cleaned_data.get("birth_date"))
        validate_phone_number(self.cleaned_data.get("phone_number"))

        return super().clean()


class AccountCreateForm(AccountBaseForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean(self) -> dict[str, Any]:
        validate_passwords(
            self.cleaned_data.get("password"), self.cleaned_data.get("confirm_password")
        )

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class AccountUpdateForm(AccountBaseForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = AccountBaseForm.Meta.fields + (
            "is_active",
            "is_staff",
            "is_superuser",
        )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("image",)
