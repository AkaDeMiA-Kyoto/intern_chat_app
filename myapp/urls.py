from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts', include('allauth.urls')),
    path('friends', views.FriendListView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('change_username', views.ChangeUsernameView.as_view(), name='change_username'),
    path('change_email', views.ChangeEmailView.as_view(), name='change_email'),
    path('change_icon', views.ChangeIconView.as_view(), name='change_icon'),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)