from django import forms

from .models import Company


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "path", "website",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter company name"}),
            "path": forms.TextInput(attrs={"placeholder": "Example: /path/to/source/"}),
            "website": forms.TextInput(attrs={"placeholder": "https://example.com"}),
        }