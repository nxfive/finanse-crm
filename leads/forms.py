from django import forms
from .models import Lead


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("first_name", "phone_number", "message", )
