from django.urls import path

from .views import list_sales, get_sale, create_sale, update_sale, delete_sale


app_name = "sales"

urlpatterns = [
    path("", list_sales, name="sale-list"),
    path("create/", create_sale, name="sale-create"),
    path("<int:pk>/", get_sale, name="sale-detail"),
    path("<int:pk>/update/", update_sale, name="sale-update"),
    path("<int:pk>/delete/", delete_sale, name="sale-delete"),
]