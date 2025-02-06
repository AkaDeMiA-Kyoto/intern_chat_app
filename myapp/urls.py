from django.urls import path
from . import views
from .views import IndexView, CustomSignupView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("friends", views.friends, name="friends"),
    path("talk_room/<int:user_id>", views.talk_room, name="talk_room"),
    path("setting", views.setting, name="setting"),
    path("change_username", views.change_username, name="change_username"),
    path("delete_user", views.delete_user, name="delete_user"),
    path("change_image", views.change_image, name="change_image"),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    path('change_email', views.change_email, name='change_email'),
]
