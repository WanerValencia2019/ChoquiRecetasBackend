from django.urls import path
from rest_framework import routers
from .api import *

#routes=routers.SimpleRouter()

#routes.register(r'login/',LoginView.as_view(),basename="register")
#print(dir(routes))
#urlpatterns += routes.get_urls()

urlpatterns=[
	path(r'register',CreateUserVIEW.as_view(),name="register"),
	path(r'login',LoginView.as_view(),name="login"),
    path(r'logout',LogoutView.as_view(),name="logout"),
    path(r'changePassword',ChangePasswordView.as_view(),name="change-password"),
    path(r'changeNames',ChangeNamesView.as_view(),name="changeNames"),
    path(r'changeUsername',ChangeUsernameView.as_view(),name="changeUsername"),
    path(r'changeEmail',ChangeEmailView.as_view(),name="changeEmail"),
    path(r'userInfo',UserInfo.as_view(),name="user-info"),
]