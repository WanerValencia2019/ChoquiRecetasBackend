from django.urls import path
from rest_framework import routers
from .api import *

#routes=routers.SimpleRouter()

#routes.register(r'login/',LoginView.as_view(),basename="register")
#print(dir(routes))
#urlpatterns += routes.get_urls()

urlpatterns=[
	path(r'register',CreateUserVIEW.as_view(),name="register"),
    path(r'update_image_profile',ChangeImageProfileView.as_view(),name="change_image_profile"),
	path(r'codeVerification',CodeVerificationView.as_view(),name="codeVerification"),
    path(r'send_code_verification',SendCodeVerification.as_view(),name="codeVerification"),
	path(r'reset_password',ResetPasswordSendCodeView.as_view(),name="reset_password_sendcode"),
	path(r'reset_password/confirm',ResetPasswordVerifyCodeView.as_view(),name="reset_password_confirm"),
	path(r'login',LoginView.as_view(),name="login"),
    path(r'logout',LogoutView.as_view(),name="logout"),
    path(r'changePassword',ChangePasswordView.as_view(),name="change-password"),
    path(r'changeNames',ChangeNamesView.as_view(),name="changeNames"),
    path(r'changeUsername',ChangeUsernameView.as_view(),name="changeUsername"),
    path(r'changeEmail',ChangeEmailView.as_view(),name="changeEmail"),
    path(r'userInfo',UserInfo.as_view(),name="user-info"),
]
