"""
URL configuration for the app_accounting application.

Defines routes for user authentication, profile management, and other key functionalities.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from app_accounting import views
from app_accounting.views import search_pages, password_reset_view, profile_view

urlpatterns = [
    # Profile management
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Core pages
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("service/", views.service, name="service"),
    path("team/", views.team, name="team"),
    path("contact/", views.contact, name="contact"),
    
    # Error pages
    path('error_404/', views.error_404, name='error_404'),

    # User authentication
    path("signin/", views.signin_view, name="signin"),
    path("signup/", views.signup_view, name="signup"),
    path("signout/", views.signout_view, name="signout"),

    # Messaging and consulting
    path("create_messaging/", views.create_messaging, name="create_messaging"),
    path("create_consulting/", views.create_consulting, name="create_consulting"),

    # Password reset
    path("password_reset/", password_reset_view, name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/custom_password_reset_confirm.html",
            success_url="/reset/done/"
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/custom_password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    # Search functionality
    path("search/", search_pages, name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
