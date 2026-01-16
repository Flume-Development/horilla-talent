"""
rest_conf.py
"""

from datetime import timedelta

from horilla import settings
from horilla.settings import INSTALLED_APPS

# Injecting installed apps to settings
# Note: rest_framework, rest_framework_simplejwt, and horilla_api are already
# defined in settings.py, so we only add drf_yasg here to avoid duplicates

REST_APPS = ["drf_yasg"]

if "drf_yasg" not in INSTALLED_APPS:
    INSTALLED_APPS.append("drf_yasg")

REST_FRAMEWORK_SETTINGS = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your Bearer token here",
        },
        "Basic": {
            "type": "basic",
            "description": "Basic authentication. Enter your username and password.",
        },
    },
    "SECURITY": [{"Bearer": []}, {"Basic": []}],
}
# Inject the REST framework settings into the Django project settings
setattr(settings, "REST_FRAMEWORK", REST_FRAMEWORK_SETTINGS)
setattr(settings, "SIMPLE_JWT", SIMPLE_JWT)
setattr(settings, "SWAGGER_SETTINGS", SWAGGER_SETTINGS)
