from django import forms
from .models import Lead


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("first_name", "phone_number", "message", "product", )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Enter lead name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter lead phone number"}),
            "message": forms.Textarea(attrs={"placeholder": "Enter lead message"})
        }


class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("first_name", "description", "email", "product", "status", )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Enter lead name"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter more information about the lead"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter lead email"})
        }
