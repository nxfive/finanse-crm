from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm, UserProfileForm
from .models import Account, UserProfile
from core.utils import paginate_queryset
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import get_random_string


@login_required
def dashboard(request: HttpRequest, username: str) -> HttpResponse:
    return render(request, "dashboard.html", {"username": username})


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                auth.login(request, user)
                return redirect("dashboard", username=user.username)
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect("login")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if Account.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.info(request, "Account with this email already exists.")
                return redirect("signup")
            
            user = Account.objects.create(username=form.cleaned_data["username"], email=form.cleaned_data["email"])

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


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    try:
        user = Account.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_superuser = True

        temporary_password = get_random_string(length=12)
        user.set_password(temporary_password)
        user.save()

        UserProfile.objects.create(user=user)

        send_mail(
            subject="Your Temporary Password",
            message=render_to_string(
                "accounts/temporary_password_email.html",
                {
                    "user": user,
                    "temporary_password": temporary_password,
                },
            ),
            from_email="no-reply@bieniasdev.com",
            recipient_list=[user.email],
        )
        messages.success(request, "Your account has been confirmed. Check your email for the temporary password.")
        return redirect("activation-complete")
    else:
        messages.error(request, "The confirmation link was invalid.")
        return redirect("activation-invalid")
    

def activation_sent(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/activation_sent.html")


def activation_complete(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/activation_complete.html")


def activation_invalid(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/activation_invalid.html")


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


@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PasswordChangeForm(request.POST, request.user)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            messages.success(request, "Password successfully changed.")
            return redirect("profile", username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/password_change.html", {"form": form})


@login_required
def update_profile(request: HttpRequest, username: str) -> HttpResponse:
    if request.user.username != username:
        raise Http404
    
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "accounts/profile_update.html", {"form": form})
