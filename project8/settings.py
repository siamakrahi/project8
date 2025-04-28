"""
Django settings for project8.

This module defines configuration settings for the Django project, including
installed apps, middleware, databases, authentication, and other essential
configurations.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Load environment variables
load_dotenv()

# considering .env files
ENV = os.getenv('DJANGO_ENV', 'dev')
env_file = f'.env.{ENV}'
load_dotenv(env_file)

# DEBUG
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY در .env تعریف نشده است!")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')  # غیرفعال کردن تشخیص خودکار HTTPS

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django.contrib.sites",
    "widget_tweaks",
    "app_accounting",
    "app_chatbot",
    "channels",
    "daphne",
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

JAZZMIN_SETTINGS = {
    "site_title": "پنل مدیریت پیشرفته",
    "site_header": "مدیریت حرفه‌ای سایت",
    "site_brand": "siamakrahi.ir",
    "site_logo": "assets/img/logo-admin.png",
    "login_logo": "assets/img/login-logo.png",
    "login_logo_dark": "assets/img/login-logo-dark.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "به پنل مدیریت پیشرفته خوش آمدید",
    "copyright": "شرکت حسابداری شما",
    "search_model": ["app_accounting.User", "app_accounting.Service"],
    
    "topmenu_links": [
        {"name": "خانه", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "مشاهده سایت", "url": "/", "new_window": True},
        {"model": "app_accounting.User"},
    ],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_accounting.Service": "fas fa-cogs",
        "app_accounting.MessagingModel": "fas fa-envelope",
        "app_accounting.ConsultingModel": "fas fa-phone-alt",
    },
    
    "theme": "lux",
    "dark_mode_theme": "darkly",
    
    "related_modal_active": True,
    "custom_css": "static/assets/css/admin-custom.css",
    "custom_js": "static/assets/js/admin-custom.js",
    "show_ui_builder": True,
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
    
    "usermenu_links": [
        {
            "name": "پشتیبانی",
            "url": "https://example.com/support",
            "new_window": True,
            "icon": "fas fa-life-ring"
        },
    ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project8.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Message settings
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Database
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGES = [
    ("fa", _("Persian")),
    ("en", _("English")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  
#EDIA_ROOT = BASE_DIR / "media"

# Authentication
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "app_accounting.User"

LOGIN_URL = "signin"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Site settings
SITE_ID = 1
SITE_NAME = os.getenv("SITE_NAME", "siamakrahi.ir")

# Email settings
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"پشتیبانی <noreply@{os.getenv('DOMAIN', '127.0.0.1')}>"
EMAIL_USE_LOCALTIME = True

# Security settings for production
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# only for dev invironment
if DEBUG:
    import socket
    ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))

# تنظیمات ASGI برای Channels
ASGI_APPLICATION = 'project8.routing.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}