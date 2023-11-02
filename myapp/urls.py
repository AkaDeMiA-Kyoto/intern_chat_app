from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:id>', views.talk_room, name='talk_room'),
    path('talk_room/<int:id>/send_message', views.send_message, name='send_message'),
    path('setting', views.setting, name='setting'),
]