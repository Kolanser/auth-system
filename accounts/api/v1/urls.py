from django.urls import path

from accounts.api.v1.views import (
    UserLoginApiView,
    UserLogoutApiView,
    UserProfileApiView,
    UserRegistrationApiView,
)

app_name = "accounts_api"

urlpatterns = [
    path("registration/", UserRegistrationApiView.as_view(), name="registration"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("logout/", UserLogoutApiView.as_view(), name="logout"),
    path("profile/", UserProfileApiView.as_view(), name="profile"),
]
