from typing import Any
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, CreateView, DetailView

from .models import Manager
from .forms import ManagerForm
from core.mixins import AdminRequiredMixin


class ManagerListView(LoginRequiredMixin, ListView):
    model = Manager
    template_name = "managers/manager_list.html"
    context_object_name = "managers"


class ManagerDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Manager
    template_name = "managers/manager_delete.html"
    success_url = reverse_lazy("managers:manager-list")


class ManagerCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = ManagerForm
    template_name = "managers/manager_create.html"
    success_url = reverse_lazy("managers:manager-list")


class ManagerDetailView(LoginRequiredMixin, DetailView):
    model = Manager
    template_name = "managers/manager_detail.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        manager = get_object_or_404(Manager, pk=kwargs.get("pk"))

        if request.user.is_superuser or manager.user == request.user:
            return super().dispatch(request, *args, **kwargs)            
            
        raise PermissionDenied("You do not have access to view this manager.")
