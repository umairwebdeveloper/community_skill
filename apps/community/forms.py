from django import forms
from .models import SkillListing, RatingAndReview, SkillRequest, UserProfile, Message
from django.contrib.auth.models import User
from datetime import time


class UserProfileForm(forms.ModelForm):
    # Add fields from the User model
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email",
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="First Name",
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Last Name",
    )

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "phone",
            "location",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Get the user instance passed to the form
        super().__init__(*args, **kwargs)
        if user:
            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            User.objects.filter(username=username)
            .exclude(pk=self.instance.user.pk)
            .exists()
        ):
            raise forms.ValidationError("This username is already taken.")
        return username


class SkillListingForm(forms.ModelForm):
    class Meta:
        model = SkillListing
        fields = [
            "title",
            "description",
            "subcategory",
            "availability_start",
            "availability_end",
            "image",
        ]
        widgets = {
            "availability_start": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "min": "09:00",
                    "max": "22:00",
                }
            ),
            "availability_end": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "min": "09:00",
                    "max": "22:00",
                }
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("availability_start")
        end = cleaned.get("availability_end")

        # only validate if both are present
        if start and end:
            # 1) end must be after start
            if end <= start:
                self.add_error(
                    "availability_end",
                    "End time must be later than start time.",
                )

            # 2) enforce the 09:00–22:00 window
            window_start = time(9, 0)
            window_end = time(22, 0)

            if start < window_start or start > window_end:
                self.add_error(
                    "availability_start",
                    "Start time must be between 09:00 and 22:00.",
                )
            if end < window_start or end > window_end:
                self.add_error(
                    "availability_end",
                    "End time must be between 09:00 and 22:00.",
                )

        return cleaned


class RatingAndReviewForm(forms.ModelForm):
    class Meta:
        model = RatingAndReview
        fields = ["rating", "review"]
        widgets = {
            "rating": forms.Select(
                attrs={"class": "form-select"},
                choices=[(i, str(i)) for i in range(1, 6)],
            ),
            "review": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your message here...",
                }
            ),
        }


class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]


class SkillRequestForm(forms.ModelForm):
    class Meta:
        model = SkillRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Why do you want to learn this skill?"}
            ),
        }
