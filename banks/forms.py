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


class BaseBankProductForm(forms.ModelForm):
    class Meta:
        model = BankProduct
        fields = ("bank", "product_type", "description", "interest_rate", "terms",)
        widgets = {
            "interest_rate": forms.NumberInput(attrs={"placeholder": "0.00"}),
        }

    def __init__(self, *args, **kwargs):
        if self.__class__ == BaseBankProductForm:
            raise NotImplementedError("BaseBankProductForm cannot be instantiated directly.")
        super().__init__(*args, **kwargs)


class BankProductCreateForm(BaseBankProductForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bank"].empty_label = "Select Bank"


class BankProductUpdateForm(BaseBankProductForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bank"].widget.attrs.update({"readonly": True, "disabled": True})
        self.fields["product_type"].widget.attrs.update({"readonly": True, "disabled": True})
