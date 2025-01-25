from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = "Create 10 random users"

    def handle(self, *args, **kwargs):
        first_names = [
            "John",
            "Jane",
            "Alice",
            "Bob",
            "Charlie",
            "Diana",
            "Edward",
            "Fiona",
            "George",
            "Hannah",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Martinez",
            "Taylor",
        ]

        for i in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = (
                f"{first_name.lower()}{last_name.lower()}{random.randint(1, 1000)}"
            )
            email = f"{username}@example.com"
            password = "password123"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Created user: {username} ({email})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {username} already exists!")
                )
