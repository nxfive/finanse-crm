from django.contrib import admin

from .models import Sale, Calculation


class SaleAdmin(admin.ModelAdmin):
    list_display = ("client", "bank_product", "sale_date", "amount", "status")


class CalculationAdmin(admin.ModelAdmin):
    list_display = ("client", "bank_product__bank", "bank_product", "amount", "duration_years", "rate")


admin.site.register(Sale, SaleAdmin)
admin.site.register(Calculation, CalculationAdmin)
