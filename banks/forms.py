from django import forms
from .models import Bank, BankProduct
from core.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("street_name", "building_number", "apartment_number", "zip_code", "city", "country",)


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ("name", "headquarters", "customer_service", "established", "chairman",)


class BankProductForm(forms.ModelForm):
    class Meta:
        model = BankProduct
        fields = ("bank", "product_type", "description", "interest_rate", "terms",)

