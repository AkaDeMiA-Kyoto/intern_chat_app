from django.urls import path, include, re_path
from django.views.static import serve
from . import views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.Index.as_view(), name='index'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:id>', views.TalkRoom.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('setting/username', views.setting_username_view, name='setting_username'),
    path('setting/email', views.setting_email_view, name='setting_email'),
    path('setting/image', views.setting_image_view, name='setting_image'),
    path('setting/password', views.SettingPassword.as_view(), name='setting_password'),
    path('setting/password/done', views.SettingPasswordDone.as_view(), name='setting_password_done'),
    path('setting/logout_completed', views.LogoutDone.as_view(), name='logout_completed'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
else:
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}))
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}))