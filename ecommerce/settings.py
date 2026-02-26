"""
Django settings for ecommerce project.

Production-ready configuration for Render.
Uses DATABASE_URL when present, otherwise SQLite locally.
"""

import os

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# Core security & environment
# ---------------------------

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-unsafe-secret-change-me")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

# Helpful if you forget to set allowed hosts on Render
# (optional but safe)
if not DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

# In production, these are good defaults on Render
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Render handles TLS; keep False unless you know you need it
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

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
    "cloudinary",
    "cloudinary_storage",
]

# ✅ Use ONLY bootstrap5 (you had both bootstrap4 and bootstrap5 set)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

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

DATABASE_URL = os.getenv("DATABASE_URL", "")

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# If Postgres, enforce SSL safely
if DATABASE_URL.startswith(("postgres://", "postgresql://")):
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].update({"sslmode": "require"})

# ---------------------------
# Password validation
# ---------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------
# Internationalization
# ---------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static & Media
# ---------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Only include STATICFILES_DIRS if the folder exists
STATICFILES_DIRS = []
_static_dir = BASE_DIR / "static"
if _static_dir.exists():
    STATICFILES_DIRS.append(_static_dir)

# WhiteNoise storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------
# Email
# ---------------------------

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

# ---------------------------
# Default primary key field type
# ---------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"