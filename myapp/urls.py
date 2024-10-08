from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView

from . import views

app_name = "myapp"
urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    path(
        'signup/',
        views.UserSignupView.as_view(),
        name='signup'
    ),
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='login'
    ),
    path(
        'friends/',
        views.friends,
        name='friends'
    ),
    path(
        'talk_room/<int:friend_id>/',
        views.talk_room,
        name='talk_room'
    ),
    path(
        'setting/',
        views.setting,
        name='setting'
    ),
    path(
        'setting/cha_name/',
        views.cha_name,
        name='cha_name'
    ),
    path(
        'setting/cha_email/',
        views.cha_email,
        name='cha_email'
    ),
    path(
        'setting/cha_image/',
        views.cha_image,
        name='cha_image'
    ),
    path(
        'setting/cha_pass/',
        views.UserPasswordChangeView.as_view(),
        name='cha_pass'
    ),
    path(
        'setting/cha_done/',
        views.cha_done,
        name='cha_done'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
