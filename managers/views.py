from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView

from .models import Manager
from .forms import ManagerForm


class ManagerListView(ListView):
    model = Manager
    template_name = "managers/manager_list.html"
    context_object_name = "managers"


class ManagerDeleteView(DeleteView):
    model = Manager
    template_name = "managers/manager_delete.html"

    def form_valid(self, form):
        user = form.instance.user
        user.is_manager = False
        user.save()
        return super().form_valid(form)



class ManagerCreateView(CreateView):
    form_class = ManagerForm
    template_name = "managers/manager_create.html"
    success_url = reverse_lazy("managers:manager-list")


    def form_valid(self, form):
        user = form.instance.user
        user.is_manager = True
        user.save()
        return super().form_valid(form)


class ManagerDetailView(DetailView):
    model = Manager
    template_name = "managers/manager_detail.html"
