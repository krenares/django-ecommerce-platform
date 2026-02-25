"""
Django settings for ecommerce project.

Production-ready configuration for Render + Neon Postgres.
Falls back to SQLite for local development.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------
# Core security & environment
# ---------------------------

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-unsafe-secret-change-me"
)

DEBUG = os.environ.get(
    "DJANGO_DEBUG",
    "False"
).lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if h.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


# ---------------------------
# Applications
# ---------------------------

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "store",
    "cart",
    "account",
    "payment",

    # Third-party
    "crispy_forms",
    "crispy_bootstrap5",
    "mathfilters",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"


# ---------------------------
# Middleware
# ---------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "ecommerce.urls"


# ---------------------------
# Templates
# ---------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.views.categories",
                "cart.context_processors.cart",
            ],
        },
    },
]


WSGI_APPLICATION = "ecommerce.wsgi.application"


# ---------------------------
# Database
# ---------------------------
# Uses Neon Postgres in production via DATABASE_URL
# Falls back to SQLite locally

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=600,
        ssl_require=False,  # IMPORTANT: don't force SSL for sqlite
    )
}

# If you want SSL for Postgres in production, do it safely:
if os.getenv("DATABASE_URL", "").startswith(("postgres://", "postgresql://")):
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}

# ---------------------------
# Password validation
# ---------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# ---------------------------
# Internationalization
# ---------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get(
    "DJANGO_TIME_ZONE",
    "UTC"
)

USE_I18N = True
USE_TZ = True


# ---------------------------
# Static & Media
# ---------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ---------------------------
# Email
# ---------------------------

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST",
    "smtp.gmail.com"
)

EMAIL_PORT = int(
    os.environ.get(
        "EMAIL_PORT",
        "587"
    )
)

EMAIL_USE_TLS = os.environ.get(
    "EMAIL_USE_TLS",
    "True"
).lower() in ("1", "true", "yes")

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    ""
)


# ---------------------------
# Default primary key field type
# ---------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"