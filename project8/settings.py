"""
Django settings for project8.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os
import socket
from pathlib import Path

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .socialaccount_providers import SOCIALACCOUNT_PROVIDERS


# ======================
# ENVIRONMENT CONFIGURATION
# ======================

# Load environment variables from .env and environment-specific .env.{ENV}
load_dotenv()
ENV = os.getenv("DJANGO_ENV", "dev")  # Default to 'dev' environment
env_file = f".env.{ENV}"
load_dotenv(env_file)


# ======================
# PATH CONFIGURATIONS
# ======================

# Build paths inside the project like: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY CONFIGURATION
# ======================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not defined in .env file!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Hosts/domain names that are valid for this site
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
if DEBUG:
    # Add current host IP when in debug mode
    ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))


# ======================
# APPLICATION DEFINITION
# ======================

INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    
    # Third-party apps
    "jazzmin",  # Admin interface
    "widget_tweaks",  # Form rendering
    "allauth",  # Authentication
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "django_otp",  # Two-factor auth
    "django_otp.plugins.otp_totp",  # TOTP (Google Authenticator)
    "otp_twilio",  # SMS-based 2FA
    "django_otp.plugins.otp_static",  # Backup codes
    "whitenoise.runserver_nostatic",  # Static files
    "parler",  # Model translations
    "rosetta",  # Translation UI
    "channels",  # WebSockets
    "daphne",  # ASGI server
    
    # Local apps
    "app_accounting",
    "app_chatbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Language detection
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_otp.middleware.OTPMiddleware",  # 2FA
    "allauth.account.middleware.AccountMiddleware",  # Allauth
    "app_accounting.middleware.LoginAttemptMiddleware",  # Custom middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project8.urls"  # Main URL configuration

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ======================
# DATABASE CONFIGURATION
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# ======================
# PASSWORD VALIDATION
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
                "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
                "MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation."
                "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
                "NumericPasswordValidator",
    },
]


# ======================
# INTERNATIONALIZATION
# ======================

LANGUAGE_CODE = "fa"  # Default language: Persian
TIME_ZONE = "Asia/Tehran"  # Iran timezone
USE_I18N = True  # Internationalization
USE_L10N = True  # Localization
USE_TZ = True  # Timezone awareness

# Supported languages
LANGUAGES = [
    ("fa", _("Persian")),
    ("en", _("English")),
]

# Translation files location
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


# ======================
# STATIC FILES (CSS, JavaScript, Images)
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = '/var/www/project8/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Collected static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Development static files
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ======================
# MEDIA FILES (Uploaded by users)
# ======================

MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/www/project8/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # User uploaded files


# ======================
# AUTHENTICATION CONFIGURATION
# ======================

AUTH_USER_MODEL = "app_accounting.User"  # Custom user model

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Default backend
    "allauth.account.auth_backends.AuthenticationBackend",  # Allauth backend
)

# Allauth settings
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5  # Max login attempts
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes lockout
ACCOUNT_PASSWORD_MIN_LENGTH = 8  # Minimum password length
ACCOUNT_EMAIL_SUBJECT_PREFIX = None  # No prefix for email subjects
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if not DEBUG else "http"
ACCOUNT_LOGOUT_ON_GET = False  # Require POST for logout
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# Custom login attempt settings
LOGIN_ATTEMPTS_LIMIT = 5
LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes in seconds

SITE_ID = 1  # Required for allauth

# Social account providers configuration
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": ""
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

# Auth URLs
LOGIN_URL = "signin"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"


# ======================
# EMAIL CONFIGURATION
# ======================

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"  # Default: console
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"Support <noreply@{os.getenv('DOMAIN', '127.0.0.1')}>"
EMAIL_USE_LOCALTIME = True

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True  # Auto-create accounts
SOCIALACCOUNT_EMAIL_REQUIRED = False  # Don't require email
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"  # Verify if email provided


# ======================
# SECURITY HEADERS
# ======================

if not DEBUG:
    # HTTPS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    
    # Cookie security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    
    # Other security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"  # Prevent clickjacking


# ======================
# TWO-FACTOR AUTHENTICATION
# ======================

OTP_TOTP_ISSUER = os.getenv("SITE_NAME", "siamakrahi.ir")  # TOTP issuer name
OTP_SMS_THROTTLE_FACTOR = 2  # SMS throttling factor

# Twilio settings for SMS 2FA
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# ======================
# JAZZMIN ADMIN CONFIG
# ======================

JAZZMIN_SETTINGS = {
    # UI Configuration
    "language_chooser": False,
    "site_header": "Admin Panel",
    "site_brand": "Site Administration",
    "site_logo": "assets/img/logo.png",
    "login_logo": "assets/img/login-logo.png",
    "login_logo_dark": "assets/img/login-logo-dark.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to Admin Panel",
    "copyright": "All rights reserved",
    
    # Theme and styling
    "theme": "lux",
    "dark_mode_theme": "darkly",
    "site_icon": "assets/img/favicon.ico",
    "custom_css": "assets/css/admin-custom.css",
    
    # Menu configuration
    "order_with_respect_to": ["auth", "app_accounting", "app_chatbot"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    
    # UI Behavior
    "show_sidebar": True,
    "navigation_expanded": True,
    "related_modal_active": True,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_accounting.Service": "fas fa-cogs",
        "app_accounting.MessagingModel": "fas fa-envelope",
        "app_accounting.ConsultingModel": "fas fa-phone-alt",
    },
    
    # User menu
    "usermenu_links": [
        {
            "name": "Logout",
            "url": "admin:logout",
            "icon": "fas fa-sign-out-alt",
            "new_window": False
        },
        {
            "name": "View Site",
            "url": "/",
            "icon": "fas fa-external-link-alt",
            "new_window": True
        }
    ],
}


# ======================
# CHANNELS (WebSockets)
# ======================

ASGI_APPLICATION = "project8.routing.application"  # ASGI config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"  # Dev-only
    }
}


# ======================
# MESSAGING SYSTEM
# ======================

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"


# ======================
# CACHE CONFIGURATION
# ======================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# ======================
# MODEL TRANSLATIONS
# ======================

PARLER_LANGUAGES = {
    1: (  # SITE_ID=1
        {"code": "fa", "name": "Persian"},  # Primary language
        {"code": "en", "name": "English"},  # Secondary language
    ),
    "default": {
        "fallback": "fa",  # Fallback to Persian
        "hide_untranslated": False,  # Show untranslated content
    }
}


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
