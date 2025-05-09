"""
URL configuration for accounting application.

Contains all URL patterns for:
- User authentication and profile management
- Core application pages
- Password reset functionality
- Two-factor authentication flows
- Search functionality
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from app_accounting import views
from app_accounting.views import (
    search_pages,
    password_reset_view,
    profile_view,
    resend_sms_code,
    verify_2fa
)


urlpatterns = [
    # -------------------------------
    # Profile Management
    # -------------------------------
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # -------------------------------
    # Core Application Pages
    # -------------------------------
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("service/", views.service, name="service"),
    path("team/", views.team, name="team"),
    path("contact/", views.contact, name="contact"),
    
    # -------------------------------
    # Error Pages
    # -------------------------------
    path("error_404/", views.error_404, name="error_404"),

    # -------------------------------
    # User Authentication
    # -------------------------------
    path("signin/", views.signin_view, name="signin"),
    path("signup/", views.signup_view, name="signup"),
    path("signout/", views.signout_view, name="signout"),

    # -------------------------------
    # Service Features
    # -------------------------------
    path("create_messaging/", views.create_messaging, name="create_messaging"),
    path("create_consulting/", views.create_consulting, name="create_consulting"),

    # -------------------------------
    # Password Reset Flow
    # -------------------------------
    path("password_reset/", password_reset_view, name="password_reset"),
    path(
        "reset/<uidb64>/<token>/", 
        views.CustomPasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"
    ),
    path(
        "reset/done/", 
        views.CustomPasswordResetCompleteView.as_view(), 
        name="password_reset_complete"
    ),

    # -------------------------------
    # Search Functionality
    # -------------------------------
    path("search/", search_pages, name="search"),
    
    # -------------------------------
    # Two-Factor Authentication
    # -------------------------------
    path("verify-2fa/", verify_2fa, name="verify_2fa"),
    path("setup_2fa/", views.setup_2fa, name="setup_2fa"),
    path("disable-2fa/", views.disable_2fa, name="disable_2fa"),
    path("setup-totp/", views.setup_totp, name="setup_totp"),
    path("verify-sms/", views.verify_sms, name="verify_sms"),
    path("resend-sms-code/", resend_sms_code, name="resend_sms_code"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
