from django.urls import path

from .views import (
    bank_finanse_create,
    bank_finanse_sent,
    house_finder_create,
    house_finder_sent,
)

app_name = "websites"

urlpatterns = [
    path("bank-finanse/", bank_finanse_create, name="bank-finanse"),
    path("bank-finanse/sent/", bank_finanse_sent, name="bank-finanse-sent"),
    path("house-finder/", house_finder_create, name="house-finder"),
    path("house-finder/sent", house_finder_sent, name="house-finder-sent"),
]
