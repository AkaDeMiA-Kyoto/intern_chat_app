from django.urls import path
from .views import (
    IndexView,
    CustomSignupView,
    FriendsListView,
    TalkRoomView,
    SettingView,
    ChangeUsernameView,
    # ChangeEmailView,
    ChangeImageView,
    DeleteUserView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    path("friends", FriendsListView.as_view(), name="friends"),
    path("talk_room/<int:user_id>", TalkRoomView.as_view(), name="talk_room"),
    path("setting", SettingView.as_view(), name="setting"),
    path("change_username", ChangeUsernameView.as_view(), name="change_username"),
    # path("change_email", ChangeEmailView.as_view(), name="change_email"),
    path("change_image", ChangeImageView.as_view(), name="change_image"),
    path("delete_user", DeleteUserView.as_view(), name="delete_user"),
]
