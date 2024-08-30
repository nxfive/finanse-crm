from django.urls import path

from .views import (
    SaleDeleteView, 
    SaleDetailView, 
    SaleListView, 
    SaleUpdateView,
    create_sale,
)


app_name = "sales"


urlpatterns = [
    path("", SaleListView.as_view(), name="sale-list"),
    path("create/", create_sale, name="sale-create"),
    path("<int:pk>/", SaleDetailView.as_view(), name="sale-detail"),
    path("<int:pk>/update/", SaleUpdateView.as_view(), name="sale-update"),
    path("<int:pk>/delete/", SaleDeleteView.as_view(), name="sale-delete"),
]