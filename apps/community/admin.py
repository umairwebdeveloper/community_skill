from django.contrib import admin
from .models import (
    SkillCategory,
    SubCategory,
    SkillListing,
    RatingAndReview,
    Message,
    UserProfile,
    SkillRequest,
)

admin.site.site_header = "Skill Listing Administration"
admin.site.site_title = "Skill Listing Admin Dashboard"
admin.site.index_title = "Welcome to the Skill Listing Management System"

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Display the name of the category in the list view
    search_fields = ("name",)  # Enable search by name
    ordering = ("name",)  # Order by name in ascending order


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")  # Display name and parent category
    search_fields = (
        "name",
        "category__name",
    )  # Enable search by subcategory and category name
    list_filter = ("category",)  # Add a filter by category in the sidebar
    ordering = ("category__name", "name")  # Order by category and then by name


@admin.register(SkillListing)
class SkillListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subcategory",
        "get_category",
        "user",
        "availability_start",
        "availability_end",
        "created_at",
    )  # Custom columns
    search_fields = (
        "title",
        "description",
        "subcategory__name",
        "subcategory__category__name",
        "user__username",
    )
    list_filter = (
        "subcategory__category",
        "subcategory",
        "created_at",
    )  # Filter by category, subcategory, and date
    ordering = (
        "subcategory__category__name",
        "subcategory__name",
        "title",
    )  # Order by category, subcategory, and title
    date_hierarchy = "created_at"  # Add a date hierarchy filter for creation dates

    def get_category(self, obj):
        return obj.subcategory.category.name

    get_category.short_description = "Category"


@admin.register(RatingAndReview)
class RatingAndReviewAdmin(admin.ModelAdmin):
    list_display = ("skill_listing", "user", "rating", "created_at")
    search_fields = ("skill_listing__title", "user__username", "review")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "skill", "content", "is_read", "timestamp")
    list_filter = ("is_read", "timestamp")
    search_fields = (
        "sender__username",
        "receiver__username",
        "skill__title",
        "content",
    )
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("sender", "receiver", "skill")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "location", "profile_image")
    search_fields = ("user__username", "phone", "location")


@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "skill", "status", "created_at")
