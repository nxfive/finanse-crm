from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .utils import company_lead_create


def bank_finanse_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(request=request, template_name="websites/bank_finanse.html", succes_url="websites:bank-finanse-sent")

def bank_finanse_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/bank_finanse_sent.html")

def house_finder_create(request: HttpRequest) -> HttpResponse:
    return company_lead_create(request=request, template_name="websites/house_finder.html", succes_url="websites:house-finder-sent")

def house_finder_sent(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="websites/house_finder_sent.html")
