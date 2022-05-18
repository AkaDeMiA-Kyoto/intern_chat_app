from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.MyLoginView.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<name>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
