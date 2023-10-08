from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:id1>/<int:id2>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_name/<int:pk>', views.change_name, name='change_name'),
    path('change_email/<int:pk>', views.change_email, name='change_email'),
    path('change_icon/<int:pk>', views.change_icon, name='change_icon'),
    path('change_pw/<int:pk>', views.change_pw, name='change_pw'),
    path('change_complete', TemplateView.as_view(template_name='myapp/change_complete.html'), name='change_complete')
    # path('setting/<int:what>', views.setting, name='setting'),
    # path('search_friends', views.search_friends, name='search_friends'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)