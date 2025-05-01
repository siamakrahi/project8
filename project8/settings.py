import os
import socket
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from .socialaccount_providers import SOCIALACCOUNT_PROVIDERS

# Load environment variables
load_dotenv()
ENV = os.getenv('DJANGO_ENV', 'dev')
env_file = f'.env.{ENV}'
load_dotenv(env_file)
          
# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY در .env تعریف نشده است!")

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
if DEBUG:
    ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    "django_otp",
    "django_otp.plugins.otp_totp",  # برای Google Authenticator
    "otp_twilio",                   # برای ارسال SMS
    "django_otp.plugins.otp_static",   # برای کدهای بازیابی
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django.contrib.sites",
    "widget_tweaks",
    "app_accounting",
    "app_chatbot",
    "channels",
    "daphne",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "parler",
    "rosetta",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "app_accounting.middleware.LoginAttemptMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project8.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        # "DIRS": [BASE_DIR / "templates"],
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
LANGUAGE_CODE = 'fa'
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ("fa", _("Persian")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
# LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  
#EDIA_ROOT = BASE_DIR / "media"

# Authentication
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "app_accounting.User"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# تنظیمات پیشرفته allauth
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 دقیقه
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_EMAIL_SUBJECT_PREFIX = None
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https' if not DEBUG else 'http'
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# تنظیمات محدودیت تلاش‌های ورود
LOGIN_ATTEMPTS_LIMIT = 5  # حداکثر تعداد تلاش‌های ناموفق
LOGIN_ATTEMPTS_TIMEOUT = 300  # زمان مسدودسازی به ثانیه (5 دقیقه)

SITE_ID = 1  # مطمئن شوید با ID سایت ایجاد شده مطابقت دارد

# تنظیمات allauth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


# مسیرهای احراز هویت
LOGIN_URL = "signin"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"


# Email settings
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"پشتیبانی <noreply@{os.getenv('DOMAIN', '127.0.0.1')}>"
EMAIL_USE_LOCALTIME = True

# جلوگیری از ایجاد حساب‌های تکراری
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'

# تنظیمات امنیتی
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# تنظیمات 2FA
OTP_TOTP_ISSUER = os.getenv('SITE_NAME', 'siamakrahi.ir')
OTP_SMS_THROTTLE_FACTOR = 2
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


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

# تنظیمات ASGI برای Channels
ASGI_APPLICATION = 'project8.routing.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Message settings
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# تنظیمات پیش‌فرض
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# تنظیمات parler
PARLER_LANGUAGES = {
    1: (  # SITE_ID=1
        {'code': 'fa', 'name': 'Persian'},
        {'code': 'en', 'name': 'English'},
    ),
    'default': {
        'fallback': 'fa',
        'hide_untranslated': False,
    }
}
