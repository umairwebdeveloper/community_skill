from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
import random
from community.models import SkillListing, SubCategory, User


class Command(BaseCommand):
    help = "Populate the SkillListing model with random data"

    def handle(self, *args, **kwargs):
        users = list(User.objects.filter(is_active=True)[:10])  # Get 10 active users
        subcategories = list(SubCategory.objects.all()[:10])  # Get 10 subcategories

        titles = [
            "Learn Professional Baking",
            "Master Python Programming",
            "Create Stunning Artwork",
            "Improve Guitar Skills",
            "Yoga for Beginners",
            "Fluent Spanish in 30 Days",
            "Build Your Own Website",
            "Effective Business Strategies",
            "Learn Photography Basics",
            "DIY Home Repairs",
        ]
        descriptions = [
            "A complete guide to mastering this skill.",
            "Suitable for beginners and intermediate learners.",
            "Learn from an experienced professional.",
            "Interactive sessions with hands-on practice.",
            "Perfect for anyone looking to improve quickly.",
        ]

        def random_datetime():
            start_date = now() + timedelta(
                days=random.randint(1, 10)
            )  # Start in next 10 days
            end_date = start_date + timedelta(
                hours=random.randint(1, 5)
            )  # End within 5 hours
            return start_date, end_date

        # Create 20 SkillListings
        for _ in range(20):
            user = random.choice(users)
            subcategory = random.choice(subcategories)
            title = random.choice(titles)
            description = random.choice(descriptions)
            availability_start, availability_end = random_datetime()

            skill = SkillListing.objects.create(
                user=user,
                title=title,
                description=description,
                subcategory=subcategory,
                availability_start=availability_start,
                availability_end=availability_end,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created SkillListing: {skill.title} ({skill.user.username})"
                )
            )
