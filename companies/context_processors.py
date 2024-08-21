from .models import Company


def companies_count(request):
    if request.user.is_authenticated:
        return {"companies_count": Company.objects.count()}
    return {}
