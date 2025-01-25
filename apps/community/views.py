from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SkillListingForm, RatingAndReviewForm, UserProfileForm, MessageForm
from django.shortcuts import get_object_or_404
from .models import SkillListing, UserProfile, Message
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


@login_required(login_url="/login")
def create_skill_listing(request):
    if request.method == "POST":
        form = SkillListingForm(request.POST, request.FILES)
        if form.is_valid():
            skill_listing = form.save(commit=False)
            skill_listing.user = request.user
            skill_listing.save()
            return redirect("user_skill_listing_list")
    else:
        form = SkillListingForm()
    return render(request, "skills/create.html", {"form": form})


@login_required(login_url="/login")
def edit_skill_listing(request, pk):
    skill_listing = get_object_or_404(SkillListing, pk=pk, user=request.user)
    if request.method == "POST":
        form = SkillListingForm(request.POST, request.FILES, instance=skill_listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill listing updated successfully!")
            return redirect("user_skill_listing_list")
    else:
        form = SkillListingForm(instance=skill_listing)
    return render(
        request,
        "skills/edit.html",
        {"form": form, "skill": skill_listing},
    )


def skill_listing_list(request):
    query = request.GET.get("q", "")  # Get the search query from the request
    skills = SkillListing.objects.all().order_by("title")

    if query:  # Filter skills if a search query exists
        skills = skills.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(subcategory__name__icontains=query)
        )

    paginator = Paginator(skills, 9)  # Show 9 skill listings per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "skills/list.html",
        {"page_obj": page_obj, "query": query, "user_list": False},
    )


def user_skill_listing_list(request):
    query = request.GET.get("q", "")  # Get the search query from the request
    skills = SkillListing.objects.filter(user=request.user).order_by("title")

    if query:  # Filter skills if a search query exists
        skills = skills.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(subcategory__name__icontains=query)
        )

    paginator = Paginator(skills, 9)  # Show 9 skill listings per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "skills/user_list.html",
        {"page_obj": page_obj, "query": query, "user_list": True},
    )


@login_required(login_url="/login")
def skill_reviews(request, pk):
    skill = get_object_or_404(SkillListing, pk=pk)
    reviews = skill.reviews.all()  # Fetch all reviews for the skill listing

    if request.method == "POST":
        form = RatingAndReviewForm(request.POST)
        if form.is_valid():
            # Check if the user has already reviewed this skill
            if skill.reviews.filter(user=request.user).exists():
                messages.error(
                    request, "You have already submitted a review for this skill."
                )
            else:
                review = form.save(commit=False)
                review.skill_listing = skill
                review.user = request.user
                review.save()
                messages.success(request, "Your review has been submitted!")
                return redirect("skill_reviews", pk=skill.pk)
    else:
        form = RatingAndReviewForm()

    return render(
        request,
        "skills/reviews.html",
        {"skill": skill, "reviews": reviews, "form": form},
    )


@login_required(login_url="/login")
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=profile, user=request.user
        )
        if form.is_valid():
            # Update user-related fields
            user = request.user
            user.username = form.cleaned_data.get("username")
            user.email = form.cleaned_data.get("email")
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.save()

            # Save profile-related fields
            form.save()
            return redirect("update_profile")  # Redirect to profile page
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, "authentication/profile.html", {"form": form})


@login_required(login_url="/login")
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).select_related(
        "skill", "sender"
    )
    paginator = Paginator(messages, 10)  # Show 9 skill listings per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "messaging/inbox.html", {"page_obj": page_obj})


@login_required(login_url="/login")
def send_messages(request):
    messages = Message.objects.filter(sender=request.user).select_related(
        "skill", "sender"
    )
    paginator = Paginator(messages, 10)  # Show 9 skill listings per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "messaging/send_messages.html", {"page_obj": page_obj})


@login_required(login_url="/login")
def skill_detail(request, skill_id):
    skill = get_object_or_404(SkillListing, id=skill_id)
    return render(request, "skills/skill_detail.html", {"skill": skill})


@login_required(login_url="/login")
def send_message(request, skill_id):
    skill = get_object_or_404(SkillListing, id=skill_id)
    messages = Message.objects.filter(skill=skill, sender=request.user).order_by("-timestamp")
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = skill.user
            message.skill = skill
            message.save()
            return redirect("send_message", skill_id=skill.id)
    else:
        form = MessageForm()
    return render(
        request,
        "messaging/send_message.html",
        {"form": form, "skill": skill, "messages": messages},
    )
