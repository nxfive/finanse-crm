from django.contrib import admin

from .models import Bank, BankProduct


class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "headquarters", "customer_service", "chairman",)

class BankProductAdmin(admin.ModelAdmin):
    list_display = ("bank", "product_type", "interest_rate",)



admin.site.register(Bank, BankAdmin)
admin.site.register(BankProduct, BankProductAdmin)
