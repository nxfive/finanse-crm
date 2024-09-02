from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Bank, BankProduct
from .utils import process_bank, process_bank_product, user_authorized


@login_required
def list_banks(request: HttpRequest) -> HttpResponse:
    if not user_authorized:
        raise Http404
    return render(request, "banks/bank_list.html", {"banks": Bank.objects.all()})
    

@login_required
def get_bank(request: HttpRequest, pk: int) -> HttpResponse:
    bank = get_object_or_404(Bank, pk=pk)

    if not user_authorized:
        raise Http404
    return render(request, "banks/bank_detail.html", {"bank": bank})


@login_required
def create_bank(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    return process_bank(request, "banks/bank_create.html")


@login_required
def update_bank(request: HttpRequest, pk: int) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    return process_bank(request, "banks/bank_update.html", pk)
   

@login_required
def delete_bank(request: HttpRequest, pk: int) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    
    bank = get_object_or_404(Bank, pk=pk)

    if request.method == "POST":
        bank.delete()

    return render(request, "banks/bank_delete.html")


@login_required
def list_banks_products(request: HttpRequest) -> HttpResponse:
    if not user_authorized:
        raise Http404
    return render(request, "banks/bank_product_list.html", {"products": BankProduct.objects.all()})


@login_required
def get_bank_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(BankProduct, pk=pk)    
    
    if not user_authorized:
        raise Http404
    
    return render(request, "banks/bank_product_detail.html", {"product": product})
        

@login_required
def create_bank_product(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404

    return process_bank_product(request, "banks/bank_product_create")


@login_required
def update_bank_product(request: HttpRequest, pk: int) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    return process_bank_product(request, "banks/bank_product_update", pk)


@login_required
def delete_bank_product(request: HttpRequest, pk: int) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404

    product = get_object_or_404(BankProduct, pk=pk)

    if request.method == "POST":
        product.delete()
    
    return render(request, "banks/bank_product_delete.html")
