from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register", views.user_register, name="register"),
    path("active/<uidb64>/<token>/", views.user_active_account, name="active_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # reset password
    path(
        "reset-password/",
        PasswordResetView.as_view(
            template_name="users/reset/password_reset.html",
            email_template_name="users/reset/password_reset_email.html",
            success_url="/accounts/reset-password-done"
        ),
        name="password_reset",
    ),
    path(
        "reset-password-done/",
        PasswordResetDoneView.as_view(template_name="users/reset/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/reset/password_reset_confirm.html",
            success_url="/accounts/reset-password-complete"

        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password-complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/reset/password_rest_complete.html"
        ),
        name="password_reset_complete",
    ),
]
