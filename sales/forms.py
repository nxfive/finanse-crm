from django import forms
from .models import Sale, Calculation


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ("client", "bank_product", "amount", "duration_years")

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client", None)
        super().__init__(*args, **kwargs)
        if self.client:
            self.fields["client"].initial = self.client
            self.fields["client"].widget.attrs["readonly"] = True

        self.fields["bank_product"].label_from_instance = self.product_label

    def product_label(self, bank_product):
        return f"{bank_product.bank}: {bank_product} - {bank_product.interest_rate}%"


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ("client", "bank_product", "amount", "duration_years")
    
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client", None)
        super().__init__(*args, **kwargs)
        if self.client:
            self.fields["client"].initial = self.client
            self.fields["client"].widget.attrs["readonly"] = True
