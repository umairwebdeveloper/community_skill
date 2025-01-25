from django import forms
from .models import SkillListing, RatingAndReview, UserProfile, Message
from django.contrib.auth.models import User


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
                attrs={"type": "time", "class": "form-control"}
            ),
            "availability_end": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        availability_start = cleaned_data.get("availability_start")
        availability_end = cleaned_data.get("availability_end")

        if (
            availability_start
            and availability_end
            and availability_end <= availability_start
        ):
            raise forms.ValidationError(
                {
                    "availability_end": "End availability time must be greater than start availability time."
                }
            )

        return cleaned_data


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
