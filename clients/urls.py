from django.urls import path
from .views import (
    list_clients,
    get_client,
    create_client,
    update_client,
    delete_client,
    process_client,
)

from sales.views import create_sale

app_name = "clients"


urlpatterns = [
    path("", list_clients, name="client-list"),
    path("create/", create_client, name="client-create"),
    path("<int:pk>/", get_client, name="client-detail"),
    path("<int:pk>/update/", update_client, name="client-update"),
    path("<int:pk>/delete/", delete_client, name="client-delete"),
    path("<int:pk>/process/", process_client, name="client-process"),
    path("<int:pk>/add-sale/", create_sale, name="client-add-sale")
]
