from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        raise PermissionDenied("You do not have permission to access this page.")