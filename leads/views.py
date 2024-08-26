from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from .forms import LeadAdminForm, LeadCreateManagerForm, LeadUpdateForm
from .models import Lead
from core.utils import paginate_queryset
from core.decorators import check_user_team


class LeadListView(ListView):
    model = Lead
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    paginate_by = 8
    agent = False

    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_superuser:
            return Lead.objects.all()
        if self.kwargs.get("agent", self.agent):
            return Lead.objects.filter(agent__user=self.request.user, team=self.team)
        if self.team:
            return Lead.objects.filter(team=self.team)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["leads"] = paginate_queryset(request=self.request, queryset=self.get_queryset(), pages=self.paginate_by)
        context["is_agent"] = self.agent
        return context


class LeadCreateView(CreateView):
    template_name = "leads/lead_create.html"

    @method_decorator(check_user_team)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.team = kwargs.pop("team", None)
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self) -> BaseModelForm:
        if self.request.user.is_superuser:
            return LeadAdminForm
        return LeadCreateManagerForm

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()

        if self.request.user.is_manager:
            kwargs["user"] = self.request.user
            kwargs["team"] = self.team
        return kwargs
    
    def get_success_url(self) -> str:
        if self.request.user.is_superuser:
            return reverse_lazy("leads:lead-list")
        return reverse_lazy("teams:leads:lead-list", kwargs={"team_slug": self.team.slug})



class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadUpdateForm
    template_name = "leads/lead_update.html"
    agent = False

    def get_success_url(self) -> str:
        return reverse_lazy("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class LeadDetailView(DetailView):
    model = Lead
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    agent = False


class LeadDeleteView(DeleteView):
    model = Lead
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead-list")
    agent = False
