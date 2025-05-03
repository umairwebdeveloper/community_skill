from django.urls import path
from . import views

urlpatterns = [
    path("skills/create/", views.create_skill_listing, name="create_skill_listing"),
    path("skills/<int:pk>/edit/", views.edit_skill_listing, name="edit_skill_listing"),
    path("skills/<int:pk>/reviews/", views.skill_reviews, name="skill_reviews"),
    path("skills/", views.skill_listing_list, name="skill_listing_list"),
    path("skills/<int:skill_id>/", views.skill_detail, name="skill_detail"),
    path("skills/user/", views.user_skill_listing, name="user_skill_listing"),
    path("profile/", views.update_profile, name="update_profile"),
    path("inbox/", views.inbox, name="inbox"),
    path("send_messages/", views.send_messages, name="send_messages"),
    path("message/send/<int:skill_id>/", views.send_message, name="send_message"),
    path("message/reply/<int:message_id>/", views.reply_message, name="reply_message"),
    path(
        "skill/<int:skill_id>/request/",
        views.send_skill_request,
        name="send_skill_request",
    ),
    path("manage-requests/", views.manage_skill_requests, name="manage_skill_requests"),
    path(
        "request/<int:request_id>/approve/",
        views.approve_skill_request,
        name="approve_skill_request",
    ),
    path(
        "request/<int:request_id>/reject/",
        views.reject_skill_request,
        name="reject_skill_request",
    ),
    path("sent-requests/", views.sent_requests, name="sent_requests"),
]
