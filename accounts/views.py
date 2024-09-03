from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm
from .models import Account
from core.utils import paginate_queryset
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


@login_required
def dashboard(request: HttpRequest, username: str) -> HttpResponse:
    return render(request, "dashboard.html", {"username": username})


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user:
                auth.login(request, user)
                return redirect("dashboard", username=user.username)
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect("login")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if Account.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.info("Account with this email already exists.")
                return redirect("signup")

            user = form.save()

            send_mail(
                subject="Activate Your Account",
                message=render_to_string(
                    "accounts/activation_email.html",
                    {
                        "user": user,
                        "protocol": "https" if request.is_secure() else "http",
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                    },
                ),
                from_email="no-reply@bieniasdev.com",
                recipient_list=[user.email],
            )
            messages.success(
                request, "Please confirm your email to complete the registration."
            )
            return redirect("activation-sent")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def list_accounts(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "accounts/account_list.html",
        {
            "accounts": paginate_queryset(
                request=request, queryset=Account.objects.all(), pages=8
            )
        },
    )
