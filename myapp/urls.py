from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', views.logout.as_view(), name='logout'),
    path("password", views.passwordchange.as_view(), name="password"),
    path("username", views.username, name="username"),
    path("username_change_done", views.username_change_done, name="username_change_done"),
    path("email", views.email, name="email"),
    path("email_change_done", views.email_change_done, name="email_change_done"),
    path("image", views.image, name="image"),
    path("image_change_done", views.image_change_done, name="image_change_done")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

