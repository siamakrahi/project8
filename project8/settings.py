"""
Django settings for project8.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""


import os
import sys
import socket
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from .socialaccount_providers import SOCIALACCOUNT_PROVIDERS


# ======================
# Environment Detection
# ======================
# Load environment variables from .env
env_name = os.getenv("DJANGO_ENV", "dev")  # Default to 'dev' environment
env_file = f".env.{env_name}"

if env_name not in ["dev", "prod"]:
    raise ValueError(f"Invalid DJANGO_ENV: {env_name}. Must be 'dev' or 'prod'.")

load_dotenv(env_file)  # بارگذاری متغیرهای مخصوص محیط


# ======================
# PATH CONFIGURATIONS
# ======================
# Build paths inside the project like: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY CONFIGURATION
# ======================
def read_secret_file(path):
    try:
        with open(path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Secret file not found at {path}")

if env_name == "dev":
    SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-unsafe-dev-key")
else:
    SECRET_KEY = read_secret_file("/etc/secrets/secret_key.txt")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host]

if DEBUG:
    ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))

SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 31536000))
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ======================
# DATABASE CONFIGURATION
# ======================
if env_name == "dev":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "makdb"),
            "USER": os.getenv("DB_USER", "mak"),
            "PASSWORD": os.getenv("DB_PASSWORD", "123456789"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DB_PASSWORD = read_secret_file("/etc/secrets/db_password.txt")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "makdb"),
            "USER": os.getenv("DB_USER", "mak"),
            "PASSWORD": DB_PASSWORD,
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }


# ======================
# APPLICATION DEFINITION
# ======================
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Admin
    'jazzmin',
    'django.contrib.admin',
    
    # 2FA
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'otp_twilio',
    
    # Internationalize
    'parler',
    'rosetta',
    
    # Dev tools
    'widget_tweaks',
    'whitenoise.runserver_nostatic',
    
    # Real-time
    'channels',
    'daphne',
    
    # Local apps
    "app_accounting",
    "app_chatbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Language detection
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
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
    {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "OPTIONS": {"user_attributes": ["username", "email"]}
}
]


# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True

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
# STATIC/MEDIA (instead of two below)
# ======================
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WHITENOISE_MANIFEST_STRICT = not DEBUG
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
WHITENOISE_USE_FINDERS = DEBUG
WHITENOISE_INDEX_FILE = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Media files (Uploaded by users)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# # ======================
# # STATIC FILES (CSS, JavaScript, Images)
# # ======================
# STATIC_URL = "/static/"
# STATIC_ROOT = '/var/www/project8/static/'
# # STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Collected static files
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),  # Development static files
# ]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# # ======================
# # MEDIA FILES (Uploaded by users)
# # ======================

# MEDIA_URL = "/media/"
# MEDIA_ROOT = '/var/www/project8/media/'
# # MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # User uploaded files


# ======================
# AUTHENTICATION CONFIGURATION
# ======================
AUTH_USER_MODEL = "app_accounting.User"

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
EMAIL_HOST_PASSWORD = read_secret_file("/etc/secrets/email_password.txt")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
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
    # Visual
    "site_title": "پنل مدیریت",
    "site_header": "پنل مدیریت",
    "site_brand": "مدیریت سایت",
    "site_logo": "admin/img/logo.png",
    "site_logo_classes": "img-square",
    "welcome_sign": "به پنل مدیریت خوش آمدید",
    "copyright": "کلیه حقوق محفوظ است",
    
    # Theme & Appearance
    "theme": "custom_theme",
    "dark_mode_theme": None,
    "site_icon": "admin/img/favicon.ico",
    "custom_css": "admin/css/admin-custom.css",
    "custom_js": "admin/js/admin-custom.js",
    
    # Custom Colors
    "custom_colors": {
        "primary": "#344E41",
        "secondary": "#A3B18A",
        "info": "#588157",
        "success": "#3A5A40",
        "warning": "#D4A017",
        "danger": "#E74A3B",
        "body": "#F9F9F8",
        "sidebar": "#F3F2EF",
    },
    
    # Menu & Navigation
    "topmenu_links": [
        {"name": "صفحه اصلی", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "مشاهده سایت", "url": "/", "new_window": True},
        {"name": "خروج", "url":"/", "signout": True},
        {"model": "auth.user"},
    ],
    
    "order_with_respect_to": [
        "auth",
        "app_accounting.خدمات",  # نمایش مستقیم خدمات
        "app_accounting",
    ],
        
    # UI Behavior
    "show_sidebar": True,
    "navigation_expanded": False,
    "related_modal_active": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_accounting.Service": "fas fa-cogs",
        "app_accounting.MessagingModel": "fas fa-comments",
        "app_accounting.ConsultingModel": "fas fa-headset",
        "sites.Site": "fas fa-globe",
    },
    
    # User Menu
    "usermenu_links": [
        {
            "name": "پروفایل",
            "url": "admin:auth_user_change",
            "icon": "fas fa-user",
        },
        {
            "name": "تغییر رمز",
            "url": "admin:auth_user_password_change",
            "icon": "fas fa-key",
        },
        {
            "name": "خروج",
            "url": "admin:logout",
            "icon": "fas fa-sign-out-alt",
        }
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
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
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 3600))

if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#     }
# }


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

# ======================
# PERFORMANCE OPTIMIZATION
# ======================
if not DEBUG:
    # Template caching
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]
    
    # Database performance
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = False
    DATABASES["default"]["CONN_MAX_AGE"] = 600
    
    # Session engine
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    
    # Security middleware
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"


# ======================
# LOGGING CONFIGURATION
# ======================
# Define environment basedon level
LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "DEBUG" if os.getenv("DJANGO_ENV") == "dev" else "INFO")

if env_name == "dev":
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'ERROR',  # تغییر از DEBUG به ERROR
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',  # لاگ‌های SQL نمایش داده نشوند
                'handlers': ['console'],
                'propagate': False,
            },
    }
    }

# #in dev only: 
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "WARNING",
#     },
# }


#@in prod only:
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#         "file": {
#             "level": "ERROR",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "/var/log/django/error.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5MB
#             "backupCount": 5,
#             "formatter": "verbose",
#         },
#     },
#     "root": {
#         "handlers": ["console", "file"],
#         "level": "WARNING",
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console", "file"],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#             "propagate": False,
#         },
#     },
# }


# ======================
# CHANNELS (WebSockets)
# ======================

ASGI_APPLICATION = "project8.routing.application"  # ASGI config

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer" if env_name == "dev" 
                 else "channels_redis.core.RedisChannelLayer",
        "CONFIG": {} if env_name == "dev" else {"hosts": [REDIS_URL]},
    }
}

# For prod only:
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"  # Dev-only
    }
}

# ======================
# HEALTH CHECKS
# ======================
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,    # in MB
}
