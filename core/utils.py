from datetime import date
from typing import Any
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.http import HttpRequest


def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def paginate_queryset(request: HttpRequest, queryset: Any, pages: int) -> Any:
    paginator = Paginator(queryset, pages)
    page = request.GET.get("page")
    try:
        paged_queryset = paginator.get_page(page)
    except PageNotAnInteger:
        paged_queryset = paginator.get_page(1)
    except (EmptyPage, InvalidPage):
        paged_queryset = paginator.page(paginator.num_pages)
    return paged_queryset
