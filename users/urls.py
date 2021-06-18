from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-passwd/", views.UpdatePasswordView.as_view(), name="password"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
    path("<int:pk>/buy", views.UserBuyView.as_view(), name="buy"),
]
