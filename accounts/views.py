from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from order.models import Order


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(request, "login.html")


def user_logout(request):
    logout(request)

    return redirect("home")


@login_required
def profile(request):

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    context = {
        "total_orders": total_orders
    }

    return render(
        request,
        "profile.html",
        context
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        request.user.first_name = request.POST.get(
            "first_name",
            ""
        )

        request.user.last_name = request.POST.get(
            "last_name",
            ""
        )

        request.user.email = request.POST.get(
            "email",
            ""
        )

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "edit_profile.html"
    )