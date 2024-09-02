from django.urls import path

from .views import (
    list_banks,
    get_bank,
    create_bank,
    update_bank,
    delete_bank,
    list_banks_products,
    get_bank_product,
    create_bank_product,
    update_bank_product,
    delete_bank_product
)


app_name = "banks"


urlpatterns = [
    path("", list_banks, name="bank-list"),
    path("create/", create_bank, name="bank-create"),
    path("<int:pk>/", get_bank, name="bank-detail"),
    path("<int:pk>/update/", update_bank, name="bank-update"),
    path("<int:pk>/delete/", delete_bank, name="bank-delete"),

    path("products/", list_banks_products, name="bank-product-list"),
    path("products/create/", create_bank_product, name="bank-product-create"),
    path("products/<int:pk>/", get_bank_product, name="bank-product-detail"),
    path("products/<int:pk>/update/", update_bank_product, name="bank-product-update"),
    path("products/<int:pk>/delete/", delete_bank_product, name="bank-product-delete"),
]