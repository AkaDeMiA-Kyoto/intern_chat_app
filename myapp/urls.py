from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import FriendsView, Login

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('signup/', views.signup, name='signup'),
    path('login/', Login.as_view(), name="login"),
    path('friends/', FriendsView.as_view(), name="friends"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)