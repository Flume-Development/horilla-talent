"""
Django settings for horilla project.
"""

import os
from os.path import join
from pathlib import Path

import environ
from django.contrib.messages import constants as messages

# Core
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(
        str,
        "django-insecure-j8op9)1q8$1&0^s&p*_0%d#pr@w9qj@1o=3#@d=a(^@9@zd@%j",
    ),
    ALLOWED_HOSTS=(list, ["*"]),
    CSRF_TRUSTED_ORIGINS=(list, ["http://localhost:8000"]),
    # S3 Storage
    AWS_ACCESS_KEY_ID=(str, None),
    AWS_SECRET_ACCESS_KEY=(str, None),
    AWS_STORAGE_BUCKET_NAME=(str, None),
    AWS_S3_REGION_NAME=(str, "af-south-1"),
    AWS_S3_FILE_OVERWRITE=(bool, False),
    AWS_S3_ADDRESSING_STYLE=(str, "virtual"),
    AWS_S3_SIGNATURE_VERSION=(str, "s3v4"),
    AWS_DEFAULT_ACL=(str, "private"),
    AWS_QUERYSTRING_AUTH=(bool, True),
    AWS_QUERYSTRING_EXPIRE=(int, 3600),
    DEFAULT_FILE_STORAGE=(str, "django.core.files.storage.FileSystemStorage"),
    MEDIA_URL=(str, "/media/"),
    MEDIA_ROOT=(str, None),
    # Email
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    EMAIL_HOST=(str, "localhost"),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_USE_SSL=(bool, False),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    DEFAULT_FROM_EMAIL=(str, "webmaster@localhost"),
    SERVER_EMAIL=(str, None),
    # Proxy
    USE_X_FORWARDED_HOST=(bool, True),
    USE_X_FORWARDED_PORT=(bool, True),
)

env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=True)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "notifications",
    "mathfilters",
    "corsheaders",
    "simple_history",
    "django_filters",
    "rest_framework",
    "rest_framework_simplejwt",
    "horilla_api",
    "base",
    "employee",
    "recruitment",
    "leave",
    "pms",
    "onboarding",
    "asset",
    "attendance",
    "payroll",
    "widget_tweaks",
    "django_apscheduler",
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "horilla.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "horilla.wsgi.application"

# Database
if env("DATABASE_URL", default=None):
    DATABASES = {
        "default": env.db(),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE", default="django.db.backends.sqlite3"),
            "NAME": env(
                "DB_NAME",
                default=os.path.join(
                    BASE_DIR,
                    "TestDB_Horilla.sqlite3",
                ),
            ),
            "USER": env("DB_USER", default=""),
            "PASSWORD": env("DB_PASSWORD", default=""),
            "HOST": env("DB_HOST", default=""),
            "PORT": env("DB_PORT", default=""),
        }
    }

# Authentication
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/login"

# Static Files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Media Files
USE_S3 = env("AWS_ACCESS_KEY_ID", default=None) is not None

if USE_S3:
    # AWS Settings from environment
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_S3_FILE_OVERWRITE = env("AWS_S3_FILE_OVERWRITE")
    AWS_S3_ADDRESSING_STYLE = env("AWS_S3_ADDRESSING_STYLE")
    AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION")
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL")
    AWS_QUERYSTRING_AUTH = env("AWS_QUERYSTRING_AUTH")
    AWS_QUERYSTRING_EXPIRE = env("AWS_QUERYSTRING_EXPIRE")
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # Set the storage backend and media URL
    DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
    MEDIA_URL = env("MEDIA_URL")
    MEDIA_ROOT = env("MEDIA_ROOT")  # Even with S3, Horilla expects this
    
    # Note: Do NOT import storage_backends here - it causes initialization errors
    # Django will handle it through DEFAULT_FILE_STORAGE setting
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = env("MEDIA_URL")
    MEDIA_ROOT = env("MEDIA_ROOT", default=os.path.join(BASE_DIR, "media/"))

# Email
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_USE_SSL = env("EMAIL_USE_SSL")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("SERVER_EMAIL", default=env("DEFAULT_FROM_EMAIL"))

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="Asia/Kolkata")
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ("en", "English (US)"),
    ("de", "Deutsche"),
    ("es", "Español"),
    ("fr", "Français"),
    ("ar", "عربى"),
    ("pt-br", "Português (Brasil)"),
    ("zh-hans", "Simplified Chinese"),
    ("zh-hant", "Traditional Chinese"),
)

LOCALE_PATHS = [
    join(BASE_DIR, "horilla", "locale"),
]

# Misc Configuration
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.DEBUG: "oh-alert--warning",
    messages.INFO: "oh-alert--info",
    messages.SUCCESS: "oh-alert--success",
    messages.WARNING: "oh-alert--warning",
    messages.ERROR: "oh-alert--danger",
}

CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

# CORS Configuration for Frontend Integration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:8080",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# JWT Token Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

SIMPLE_HISTORY_REVERT_DISABLED = True

DJANGO_NOTIFICATIONS_CONFIG = {
    "USE_JSONFIELD": True,
    "SOFT_DELETE": True,
    "USE_WATCHED": True,
    "NOTIFICATIONS_STORAGE": "notifications.storage.DatabaseStorage",
    "TEMPLATE": "notifications.html",
}

X_FRAME_OPTIONS = "SAMEORIGIN"

# Production Security
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")
    USE_X_FORWARDED_PORT = env("USE_X_FORWARDED_PORT")
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = False  # ALB handles redirects
else:
    USE_X_FORWARDED_HOST = False
    USE_X_FORWARDED_PORT = False
