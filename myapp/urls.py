from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:id>', views.TalkRoom.as_view(), name='talk_room'),
    path('setting', views.setting_view, name='setting'),
    path('setting/username', views.setting_username_view, name='setting_username'),
    path('setting/email', views.setting_email_view, name='setting_email'),
    path('setting/image', views.setting_image_view, name='setting_image'),
    path('setting/password', views.SettingPassword.as_view(), name='setting_password'),
    path('setting/password/done', views.SettingPasswordDone.as_view(), name='setting_password_done'),
    path('setting/logout', views.Logout.as_view(), name='logout_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
