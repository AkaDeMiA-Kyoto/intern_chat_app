from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('logout', views.logout_view.as_view(), name='logout_view'),
    path('username_update', views.username_update, name='username_update_view'),
    path('email_update', views.email_update, name='email_update_view'),
    path('img_update', views.img_update, name='img_update_view'),
    path('done', views.update_done, name='done_view'),
    path('password_update', views.password_update_view.as_view(), name='password_update_view'),
    path('password_update_done', views.password_update_done_view.as_view(), name='password_update_done_view'),
    path('friends', views.FriendsListView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)