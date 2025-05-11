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


SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]


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
    
    # احراز هویت و امنیت
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'otp_twilio',
    
    # بین‌المللی‌سازی
    'parler',
    'rosetta',
    
    # ابزارهای توسعه
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
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "OPTIONS": {
            "connect_timeout": 3,
            "sslmode": "require" if not DEBUG else "prefer",
            "application_name": "project8",
        },
        "CONN_MAX_AGE": 300 if not DEBUG else 0,
        "DISABLE_SERVER_SIDE_CURSORS": False,
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
# STATIC/MEDIA
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
    # هویت بصری
    "site_title": "پنل مدیریت",  # عنوان تب مرورگر
    "site_header": "پنل مدیریت",  # هدر صفحه
    "site_brand": "مدیریت سایت",  # برند نمایشی
    "site_logo": "admin/img/logo.png",  # مسیر نسبی از STATIC_URL
    "login_logo": None,  # استفاده از همان site_logo
    "login_logo_dark": None,  # استفاده از تم تاریک
    "site_logo_classes": "img-square",  # بهتر از img-circle برای لوگوهای رسمی
    "welcome_sign": "به پنل مدیریت خوش آمدید",  # متن خوشآمدگویی
    "copyright": "کلیه حقوق محفوظ است",  # متن کپی رایت
    
    # تم و ظاهر
    "theme": "flatly",  # تم پیشنهادی (ساده‌تر از lux)
    "dark_mode_theme": "darkly",  # تم تاریک
    "site_icon": "admin/img/favicon.ico",  # آیکون سایت
    "custom_css": "admin/css/custom.css",  # css سفارشی
    
    # منوها و ناوبری
    "topmenu_links": [
        {"name": "صفحه اصلی", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "مشاهده سایت", "url": "/", "new_window": True},
        {"model": "auth.user"},  # لینک مستقیم به مدل کاربر
        {"app": "app_accounting"},  # لینک مستقیم به اپ حسابداری
    ],
    
    # رفتار رابط کاربری
    "show_sidebar": True,  # نمایش نوار کناری
    "navigation_expanded": False,  # منوها به صورت پیش‌فرض جمع باشند
    "related_modal_active": True,  # استفاده از مودال برای روابط
    "show_ui_builder": False,  # غیرفعال در production
    "changeform_format": "horizontal_tabs",  # فرمت فرم‌ها
    
    # آیکون‌ها
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_accounting.Service": "fas fa-cogs",
        "app_accounting.MessagingModel": "fas fa-comments",
        "app_accounting.ConsultingModel": "fas fa-headset",
        "sites.Site": "fas fa-globe",
    },
    
    # منوی کاربر
    "usermenu_links": [
        {
            "name": "پروفایل",
            "url": "admin:auth_user_change",  # لینک به پروفایل کاربر
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
    
    # تنظیمات پیشرفته
    "language_chooser": True,  # فعال برای چندزبانه
    "order_with_respect_to": [
        "auth",
        "auth.user",
        "auth.group",
        "app_accounting",
        "app_chatbot",
        "sites.site",
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

if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
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
    DATABASES["default"]["CONN_MAX_AGE"] = 300
    
    # Session engine
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    
    # Security middleware
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# ======================
# LOGGING CONFIGURATION
# ======================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/django/error.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

# ======================
# HEALTH CHECKS
# ======================
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,    # in MB
}