from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from .models import Agent
from .forms import AgentCreateForm, AgentUpdateForm


class AgentListView(ListView):
    model = Agent
    template_name = "agents/agent_list.html"
    context_object_name = "agents"


class AgentCreateView(CreateView):
    form_class = AgentCreateForm
    template_name = "agents/agent_create.html"
    success_url = reverse_lazy("agents:agent-list")


class AgentUpdateView(UpdateView):
    model = Agent
    form_class = AgentUpdateForm
    template_name = "agents/agent_update.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy("agents:agent-detail", kwargs={"pk": self.kwargs["pk"]})
    

class AgentDetailView(DetailView):
    model = Agent
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"


class AgentDeleteView(DeleteView):
    model = Agent
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    success_url = reverse_lazy("agents:agent-list")
