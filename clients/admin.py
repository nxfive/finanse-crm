from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "email", "phone_number", "birth_date", "salary",)
    

admin.site.register(Client, ClientAdmin)
