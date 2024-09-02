from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Calculation, Sale
from .forms import SaleForm, CalculationForm
from .utils import calculate_monthly_payment

from core.decorators import check_user_team
from core.utils import paginate_queryset
from clients.models import Client
from teams.models import Team


@login_required
@check_user_team
def list_sales(request: HttpRequest, **kwargs) -> HttpResponse:
    team = kwargs.pop("team", None)

    if request.user.is_superuser:
        queryset = Sale.objects.all()
    
    else:
        if not team or (team.team_type == Team.TeamTypes.SUPPORT):
            raise Http404

        elif request.user.is_manager:
            queryset = Sale.objects.filter(client__team=team)

        else:
            queryset = Sale.objects.filter(client__user=request.user)

    return render(request, "sales/sale_list.html", {"sales": paginate_queryset(request, queryset, 8)})


@login_required
def get_sale(request: HttpRequest, pk: int) -> HttpResponse:
    sale = get_object_or_404(Sale, pk=pk)

    if not (request.user.is_superuser or sale.client.user == request.user or (sale.client.team and sale.client.team.manager.user == request.user)):
        raise Http404

    return render(request, "sales/sale_delete.html", {"sale": sale})


@login_required
def update_sale(request: HttpRequest, pk: int) -> HttpResponse:
    sale = get_object_or_404(Sale, pk=pk)

    if not (request.user.is_superuser or sale.client.user == request.user or (sale.client.team and sale.client.team.manager.user == request.user)):
        raise Http404
    
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
        return redirect("sales:sale-detail", pk=sale.pk)
    else:
        form = SaleForm(instance=sale)
    return render(request, "sales/sale_update.html", {"form": form})


@login_required
def create_sale(request: HttpRequest, pk: int = None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    if request.method == "POST":
        if request.POST.get("action") == "calculate":
            form = CalculationForm(request.POST, client=client)
            if form.is_valid():
                bank_product = form.cleaned_data.get("bank_product")
                amount = form.cleaned_data.get("amount")
                duration_years = form.cleaned_data.get("duration_years")

                if Calculation.objects.filter(
                        client=client,
                        bank_product=bank_product,
                        amount=amount,
                        duration_years=duration_years).exists():
                    messages.info(request, "This calculation already exists.")
                    return render(request, "sales/sale_create.html", {"form": form, "client": client})

                if amount and duration_years and bank_product:
                    calculate = form.save(commit=False)
                    calculate.rate = round(calculate_monthly_payment(amount=amount, interest_rate=bank_product.interest_rate, years=duration_years), 2)
                    form.save()
                    messages.info(request, "Calculation added.")
                    return render(request, "sales/sale_create.html", {"form": form, "client": client})

        elif request.POST.get("action") == "create":
            form = SaleForm(request.POST, client=client)
            if form.is_valid():
                form.save()
                messages.info(request, "You successfully created a sale")
                if pk:
                    return redirect("clients:client-add-sale", pk=pk)
                else:
                    return redirect("sales:sale-create")
    else:
        form = SaleForm(client=client)

    return render(request, "sales/sale_create.html", {"form": form, "client": client})


@login_required
def delete_sale(request: HttpRequest, pk: int) -> HttpResponse:
    sale = get_object_or_404(Sale, pk=pk)

    if not (request.user.is_superuser or sale.client.user == request.user or (sale.client.team and sale.client.team.manager.user == request.user)):
        raise Http404

    if request.method == "POST":
        sale.delete()
        return redirect("sales:sale-list") 

    return render(request, "sales/sale_delete.html", {"sale": sale})   
