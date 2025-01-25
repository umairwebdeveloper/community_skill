from django.urls import path
from . import views

urlpatterns = [
    path("skills/create/", views.create_skill_listing, name="create_skill_listing"),
    path("skills/<int:pk>/edit/", views.edit_skill_listing, name="edit_skill_listing"),
    path("skills/<int:pk>/reviews/", views.skill_reviews, name="skill_reviews"),
    path("skills/", views.skill_listing_list, name="skill_listing_list"),
    path("skills/<int:skill_id>/", views.skill_detail, name="skill_detail"),
    path("skills/user/", views.user_skill_listing_list, name="user_skill_listing_list"),
    path("profile/", views.update_profile, name="update_profile"),
    path("inbox/", views.inbox, name="inbox"),
    path("send_messages/", views.send_messages, name="send_messages"),
    path("message/send/<int:skill_id>/", views.send_message, name="send_message"),
]
