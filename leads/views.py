from typing import Any
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from .forms import LeadCreateForm, LeadUpdateForm
from .models import Lead
from core.utils import paginate_queryset


class LeadListView(ListView):
    model = Lead
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    paginate_by = 8

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["leads"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        return context


class LeadCreateView(CreateView):
    form_class = LeadCreateForm
    template_name = "leads/lead_create.html"
    success_url = reverse_lazy("leads:lead-list")


class LeadUpdateView(UpdateView):
    model = Lead
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
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead-list")
