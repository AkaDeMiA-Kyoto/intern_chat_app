from django.urls import path
from . import views
from .views import CustomPasswordChangeView, IndexView, CustomSignupView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("friends", views.friends, name="friends"),
    path("talk_room/<int:user_id>", views.talk_room, name="talk_room"),
    path("setting", views.setting, name="setting"),
    path("change_username", views.change_username, name="change_username"),
    path("delete_user", views.delete_user, name="delete_user"),
    path("change_image", views.change_image, name="change_image"),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    # path('change_email', views.change_email, name='change_email'),
    # path('change_password', CustomPasswordChangeView.as_view(), name='change_password'),
    # path('signup', SignUpView.as_view(), name='signup_view'),
    # path('login', CustomLoginView.as_view(), name='login'),
    # path('logout', LogoutView.as_view(), name='logout'),
]
