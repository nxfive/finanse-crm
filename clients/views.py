from django.utils import timezone
from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from teams.models import Team
from .forms import ClientAgentForm, ClientForm
from .models import Client
from leads.models import Lead
from core.decorators import check_user_team
from core.utils import paginate_queryset
from .utils import calculate_creditworthiness
from django.contrib.auth.decorators import login_required
from datetime import timedelta


@login_required
@check_user_team
def list_clients(request: HttpRequest, **kwargs) -> HttpResponse:
    team = kwargs.pop("team", None)

    if request.user.is_superuser:
        queryset = Client.objects.all()
    
    else:
        if not team or (team.team_type == Team.TeamTypes.SUPPORT):
            raise Http404

        elif request.user.is_manager:
            queryset = Client.objects.filter(team=team)

        else:
            queryset = Client.objects.filter(user=request.user)

    return render(request, "clients/client_list.html", {"clients": paginate_queryset(request, queryset, 8)})


def get_client(request: HttpRequest, pk: int) -> HttpResponse:
    client = get_object_or_404(Client, pk=pk)
    
    if not (request.user.is_superuser or client.user == request.user or (client.team and client.team.manager.user == request.user)):
        raise Http404
        
    return render(request, "clients/client_detail.html", {"client": client})


@login_required
@check_user_team
def create_client(request: HttpRequest, pk: int=None, **kwargs):
    team = kwargs.pop("team", None)
    
    if not request.user.is_superuser:
        if not team or team and team.team_type == Team.TeamTypes.SUPPORT:
            raise Http404 
        
    if pk:
        lead = get_object_or_404(Lead, pk=pk)
        client = Client.objects.filter(phone_number=lead.phone_number)
        if client.exists():
            return redirect("clients:client-detail", pk=client.first().pk)
        else:
            if request.method == "POST":
                form = ClientForm(request.POST, user=request.user, lead=lead)
                if form.is_valid():
                    client = form.save(commit=False)
                    client.user = request.user
                    client.save()
                    lead.status = Lead.LeadStatus.CLOSED
                    lead.save()

                    messages.success(request, "Client successfully created.")
                    return redirect("clients:client-detail", pk=client.pk)
            else:
                form = ClientForm(lead=lead)
            return render(request, "clients/client_create.html", {"form": form, "lead": lead})
    else:
        if request.method == "POST":
            form = ClientForm(request.POST)
            if form.is_valid():
                client = form.save()
                messages.success(request, "Client successfully created.")
                return redirect("clients:client-detail", pk=client.pk)
        else:
            form = ClientForm()
        return render(request, "clients/client_form.html", {"form": form})
        

@login_required
def update_client(request: HttpRequest, pk: int) -> HttpResponse:
    client = get_object_or_404(Client, pk=pk)
    
    if not (request.user.is_superuser or client.user == request.user or (client.team and client.team.manager.user == request.user)):
        raise Http404
    
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client, user=request.user) if request.user.is_superuser or request.user.is_manager else ClientAgentForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
        
        return redirect("clients:client-detail", pk=client.pk)
    else:
        form = ClientForm(instance=client, user=request.user) if request.user.is_superuser or request.user.is_manager else ClientAgentForm(instance=client)
    return render(request, "clients/client_update.html", {"form": form, "client": client})
    

@login_required
def delete_client(request: HttpRequest, pk: int) -> HttpResponse:
    client = get_object_or_404(Client, pk=pk)

    if not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        client.delete()
        return redirect("clients:client_list")
    
    return render(request, "clients/client_detail", {"client": client})


@login_required
def process_client(request: HttpRequest, pk: int) -> HttpResponse:
    client = get_object_or_404(Client, pk=pk)

    if not (request.user.is_superuser or client.user == request.user or (client.team and client.team.manager.user == request.user)):
        raise Http404
        
    if client.processing_date and (timezone.now() - client.processing_date) <= timedelta(days=15):
        messages.info(request, "Creditworthiness cannot be recalculated within 15 days of the last process.")
        return redirect("clients:client-detail", pk=pk)

    client.creditworthiness = calculate_creditworthiness(client)
    client.processing_date = timezone.now()
    client.save()

    return redirect("clients:client-detail", pk=pk)