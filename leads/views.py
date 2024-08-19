from django.urls import reverse_lazy
from .forms import LeadCreateForm, LeadUpdateForm
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

from .models import Lead


class LeadListView(ListView):
    model = Lead
    template_name = "leads/lead_list.html"
    context_object_name = "leads"


class LeadCreateView(CreateView):
    form_class = LeadCreateForm
    template_name = "leads/lead_create.html"
    success_url = reverse_lazy("leads:lead-list")


class LeadUpdateView(UpdateView):
    form_class = LeadUpdateForm
    template_name = "leads/lead_update.html"

    def get_success_url(self) -> str:
        return reverse_lazy("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})


class LeadDetailView(DetailView):
    model = Lead
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"


class LeadDeleteView(DeleteView):
    model = Lead
    template_name = "leads/lead_delete.html"
    context_object_name = "leads"
    success_url = reverse_lazy("leads:lead-list")
