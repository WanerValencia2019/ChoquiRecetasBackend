from django.urls import path
from rest_framework import routers
from . import api

#routes=routers.SimpleRouter()

#routes.register(r'login/',LoginView.as_view(),basename="register")
#print(dir(routes))
#urlpatterns += routes.get_urls()

urlpatterns=[
	path(r'register',api.CreateUserVIEW.as_view(),name="register"),
    path(r'update_image_profile',api.ChangeImageProfileView.as_view(),name="change_image_profile"),
	path(r'codeVerification',api.CodeVerificationView.as_view(),name="codeVerification"),
    path(r'send_code_verification',api.SendCodeVerification.as_view(),name="codeVerification"),
	path(r'reset_password',api.ResetPasswordSendCodeView.as_view(),name="reset_password_sendcode"),
	path(r'reset_password/confirm',api.ResetPasswordVerifyCodeView.as_view(),name="reset_password_confirm"),
	path(r'login',api.LoginView.as_view(),name="login"),
    path(r'logout',api.LogoutView.as_view(),name="logout"),
    path(r'changePassword',api.ChangePasswordView.as_view(),name="change-password"),
    path(r'changeNames',api.ChangeNamesView.as_view(),name="changeNames"),
    path(r'changeUsername',api.ChangeUsernameView.as_view(),name="changeUsername"),
    path(r'changeEmail',api.ChangeEmailView.as_view(),name="changeEmail"),
    path(r'user_profile',api.UserProfileView.as_view(),name="user-profile"),
]
