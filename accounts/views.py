from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import LoginForm


@login_required
def dashboard(request, username):
    return render(request, "dashboard.html", {"username": username})


def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(request, username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard", username=user.username)
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect("login")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})