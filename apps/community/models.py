from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class SkillCategory(models.Model):
    """
    Represents a broad category of skills (e.g., Cooking, Technology).
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Skill Category",
        help_text="Enter the name of the skill category (e.g., Cooking, Technology).",
    )

    class Meta:
        ordering = ["name"]  # Default ordering by name for easier readability
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Represents subcategories under a specific skill category (e.g., Baking under Cooking).
    """

    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Parent Category",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Subcategory",
        help_text="Enter the subcategory name (e.g., Baking, Web Development).",
    )

    class Meta:
        ordering = ["category__name", "name"]  # Order by parent category and then name
        unique_together = (
            "category",
            "name",
        )  # Ensure unique subcategories within a category
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class SkillListing(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name="Skill Sharer",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Skill Title",
        help_text="Enter a descriptive title for the skill (e.g., Mastering the Art of Baking).",
    )
    description = models.TextField(
        verbose_name="Skill Description",
        help_text="Provide a detailed description of the skill being offered.",
    )
    subcategory = models.ForeignKey(
        "SubCategory",
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name="Skill Subcategory",
    )
    availability_start = models.TimeField(
        verbose_name="Start Availability",
        help_text="Specify the start time when you're available for sessions.",
    )
    availability_end = models.TimeField(
        verbose_name="End Availability",
        help_text="Specify the end time when you're available for sessions.",
    )
    image = models.ImageField(
        upload_to="skill_images/",
        verbose_name="Skill Image",
        help_text="Upload an image related to the skill.",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ["subcategory__category__name", "subcategory__name", "title"]
        verbose_name = "Skill Listing"
        verbose_name_plural = "Skill Listings"

    def __str__(self):
        return f"{self.title} ({self.subcategory.name})"

    def get_full_category(self):
        return f"{self.subcategory.category.name} > {self.subcategory.name}"

    def average_rating(self):
        reviews = self.reviews.all()  # Access related reviews
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 2)  # Average rating rounded to 2 decimals
        return None

    def total_reviews(self):
        return self.reviews.count()


class RatingAndReview(models.Model):
    """
    Represents a rating and review for a skill listing by a user.
    """

    skill_listing = models.ForeignKey(
        "SkillListing",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Skill Listing",
        help_text="The skill listing being reviewed.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Reviewer",
        help_text="The user providing the review.",
    )
    rating = models.PositiveIntegerField(
        verbose_name="Rating",
        help_text="Provide a rating between 1 and 5.",
        choices=[(i, str(i)) for i in range(1, 6)],  # Choices for a 1-5 rating scale
    )
    review = models.TextField(
        verbose_name="Review",
        help_text="Provide your feedback on the skill.",
        blank=True,  # Review is optional
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        unique_together = (
            "skill_listing",
            "user",
        )  # Prevent duplicate reviews for the same skill by the same user
        ordering = ["-created_at"]  # Latest reviews appear first
        verbose_name = "Rating and Review"
        verbose_name_plural = "Ratings and Reviews"

    def __str__(self):
        return f"Review by {self.user.username} for {self.skill_listing.title} ({self.rating}/5)"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Sender",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name="Receiver",
    )
    skill = models.ForeignKey(
        "SkillListing",
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Skill",
    )
    content = models.TextField(verbose_name="Message Content")
    is_read = models.BooleanField(default=False, verbose_name="Read Status")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} about {self.skill.title}"
