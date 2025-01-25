from django.core.management.base import BaseCommand
from community.models import SkillCategory, SubCategory


class Command(BaseCommand):
    help = "Populate SkillCategory and SubCategory with random data"

    def handle(self, *args, **kwargs):
        categories = [
            "Cooking",
            "Technology",
            "Art",
            "Music",
            "Fitness",
            "Languages",
            "DIY",
            "Business",
        ]

        subcategories = {
            "Cooking": ["Baking", "Grilling", "Vegetarian Cooking", "Pastry Making"],
            "Technology": [
                "Web Development",
                "Data Science",
                "Cybersecurity",
                "AI & ML",
            ],
            "Art": ["Painting", "Sketching", "Sculpture", "Digital Art"],
            "Music": ["Guitar", "Piano", "Drums", "Music Composition"],
            "Fitness": ["Yoga", "Weightlifting", "Cardio", "Martial Arts"],
            "Languages": ["English", "Spanish", "French", "Japanese"],
            "DIY": ["Woodworking", "Knitting", "Home Repairs", "Gardening"],
            "Business": ["Marketing", "Accounting", "Entrepreneurship", "Leadership"],
        }

        for category_name in categories:
            category, created = SkillCategory.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_name}")
                )

            for subcategory_name in subcategories[category_name]:
                subcategory, sub_created = SubCategory.objects.get_or_create(
                    category=category, name=subcategory_name
                )
                if sub_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Created subcategory: {subcategory_name} under {category_name}"
                        )
                    )
