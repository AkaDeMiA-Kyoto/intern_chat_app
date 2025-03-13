from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name='myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends_view, name='friends'),
    path('talk_room/<int:id>', views.talk_room, name='talk_room'),
    path('setting', views.setting_view, name='setting'),
    path('logout', views.logout_view, name='logout_view'),
    path('setting/change_name', views.ChangeNameView.as_view(), name='change_name'),
    path('setting/change_mail', views.ChangeMailView.as_view(), name='change_mail'),
    path('setting/change_icon', views.ChangeIconView.as_view(), name='change_icon'),
    path('setting/change_password', auth_views.PasswordChangeView.as_view(template_name = 'myapp/change_password.html', success_url=reverse_lazy('myapp:change_password_done')), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myapp/change_password_done.html'), name='change_password_done'),
]
