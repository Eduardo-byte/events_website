from django.urls import path
from . import views
from django.conf.urls import url



urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register"),
    path('change_password', views.change_password, name='change-password'),
]