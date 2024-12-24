from django.urls import path
from . import views
from .views import CustomLoginView,CustomPasswordChangeView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change_username', views.change_username, name='change_username'),
    path('change_email', views.change_email, name='change_email'),
    path('change_image', views.change_image, name='change_image'),
    path('change_password', CustomPasswordChangeView.as_view(), name='change_password'),
    path('delete_user', views.delete_user, name='delete_user'),
]
