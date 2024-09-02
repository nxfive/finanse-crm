from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from agents.models import Agent
from teams.models import Team

from .models import Bank, BankProduct
from .forms import AddressForm, BankForm, BankProductForm


def process_bank_product(request: HttpRequest, template_name: str, pk: int=None) -> HttpResponse:
    product = get_object_or_404(BankProduct, pk=pk) if pk else None 

    if request.method == "POST":
        form = BankProductForm(request.POST, instance=product) if pk else BankProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect("banks:bank-product-detail", pk=product.pk)
    else:
        form = BankProductForm(instance=product) if pk else BankProductForm()
    return render(request, template_name, {"form": form})


def process_bank(request: HttpRequest, template_name: str, pk: int=None) -> HttpResponse:
    bank = get_object_or_404(Bank, pk=pk) if pk else None
    address = bank.address if bank else None

    if request.method == "POST":
        bank_form = BankForm(request.POST, instance=bank) if pk else BankForm(request.POST)
        address_form = AddressForm(request.POST, instance=address) if pk else AddressForm(request.POST)
        
        if bank_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            
            bank = bank_form.save(commit=False)
            bank.address = address
            bank.save()
            
            return redirect("banks:bank-detail", pk=bank.pk)
    else:
        bank_form = BankForm(instance=bank) if pk else BankForm()
        address_form = AddressForm(instance=address) if pk else AddressForm()
    
    return render(request, template_name, {"bank_form": bank_form, "address_form": address_form})


def user_authorized(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        sales_manager_ids = Team.objects.filter(team_type=Team.TeamTypes.SALES).values_list("manager__user__id", flat=True)
        sales_agent_ids = Agent.objects.filter(team__team_type=Team.TeamTypes.SALES).values_list("user__id", flat=True)

        return request.user.id in sales_manager_ids or request.user.id in sales_agent_ids