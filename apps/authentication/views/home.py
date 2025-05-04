from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    top_categories = [
        {"name": "Design", "slug": "design", "icon": "fas fa-paint-brush"},
        {"name": "Photography", "slug": "photography", "icon": "fas fa-camera-retro"},
        {"name": "Cooking", "slug": "cooking", "icon": "fas fa-utensils"},
        {"name": "Music", "slug": "music", "icon": "fas fa-music"},
        {"name": "Programming", "slug": "programming", "icon": "fas fa-code"},
        {"name": "Yoga", "slug": "yoga", "icon": "fas fa-person-praying"},
    ]
    featured_instructors = [
        {
            "name": "Alice Johnson",
            "expertise": "Graphic Design",
            "icon": "fas fa-palette",
        },
        {
            "name": "Marcus Lee",
            "expertise": "Digital Marketing",
            "icon": "fas fa-bullhorn",
        },
        {
            "name": "Priya Singh",
            "expertise": "Yoga & Mindfulness",
            "icon": "fas fa-spa",
        },
        {
            "name": "Carlos Ramirez",
            "expertise": "Photography",
            "icon": "fas fa-camera-retro",
        },
    ]
    testimonials = [
        {
            "quote": "This platform changed my life!",
            "author_name": "Jane D.",
            "rating": 5,
        },
        {
            "quote": "I learned guitar from scratch here.",
            "author_name": "Tom R.",
            "rating": 4,
        },
        {
            "quote": "The community is incredibly supportive.",
            "author_name": "Sara K.",
            "rating": 5,
        },
    ]
    context = {
        "top_categories": top_categories,
        "featured_instructors": featured_instructors,
        "testimonials": testimonials,
        "star_range": range(1, 6),
    }
    return render(request, "home/home.html", context)


def about(request):
    return render(request, "home/about.html")


@login_required(login_url="/login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            messages.success(request, "Your password was succesfully updated!")
            return redirect("home")
        else:
            messages.error(request, "Ops, an error ocurred! Please, try again :)")

    form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "home/change_password/change_password.html", context)
