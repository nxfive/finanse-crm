from django.contrib import admin


class BaseUserAdmin(admin.ModelAdmin):
    """
        Base admin class for user-related models.

        This class should only be used as a base class for other ModelAdmin classes
        and should not be registered directly with the Django admin site.
    """
    list_display = ("get_last_name", "get_first_name", "get_email",)
    list_display_links = ("get_last_name", "get_email",)

    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_email(self, obj):
        return obj.user.email
    
    get_last_name.short_description = "Last Name"
    get_first_name.short_description = "First Name"
    get_email.short_description = "Email"
