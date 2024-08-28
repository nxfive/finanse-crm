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
