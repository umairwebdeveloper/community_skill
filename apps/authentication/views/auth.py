from django.shortcuts import render, redirect
from ..forms import LoginForm, SignUpForm
from django.contrib import auth, messages
from django.contrib.auth.models import User


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.save()
            messages.success(request, "User registered successfully!")
            return redirect("login")
        else:
            for value in form.errors.values():
                messages.error(request, f"{value}")

    if request.user.is_authenticated:
        return redirect("home")

    form = SignUpForm()
    context = {"form": form}
    return render(request, "authentication/signup.html", context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data.get(
                "email"
            )  # This could be email or username
            password = form.cleaned_data.get("password")

            # Check if the identifier is an email or a username
            if User.objects.filter(email=identifier).exists():
                # Login using email
                username = (
                    User.objects.filter(email=identifier)
                    .values_list("username", flat=True)
                    .get()
                )
                user = auth.authenticate(request, username=username, password=password)
            else:
                # Login using username
                user = auth.authenticate(
                    request, username=identifier, password=password
                )

            if user is not None:
                auth.login(request, user)
                return redirect("home")
            else:
                messages.error(
                    request,
                    "Incorrect username/email or password! Verify and try again.",
                )
                return redirect("login")

    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm()
    context = {"form": form}
    return render(request, "authentication/login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("home")
