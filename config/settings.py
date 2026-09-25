"""
Django settings for the Fake Internship Detection System.

Mirrors the configuration surface of the original Flask backend
(backend/config.py in the Flask+HTML version): model artefact paths,
defer thresholds, dataset path - all still read from environment
variables via python-dotenv so nothing sensitive is hard-coded.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    "apps.accounts",
    "apps.advertisements",
    "apps.detection",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ---------------------------------------------------------------------------
# CORS - allow the React (Vite) dev server to call this API
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------------------------
# ML / model configuration (mirrors backend/config.py from the Flask build)
# ---------------------------------------------------------------------------
BASELINE_MODEL_PATH = BASE_DIR / os.getenv(
    "BASELINE_MODEL_PATH", "models/baseline/tfidf_logreg.joblib"
)
TRANSFORMER_MODEL_PATH = BASE_DIR / os.getenv("TRANSFORMER_MODEL_PATH", "models/transformer/")
INTEGRATED_MODEL_PATH = BASE_DIR / os.getenv(
    "INTEGRATED_MODEL_PATH", "models/integrated/integrated_model.joblib"
)
ACTIVE_MODEL_VERSION = os.getenv("ACTIVE_MODEL_VERSION", "baseline-v0")

DEFER_THRESHOLD_LOW = float(os.getenv("DEFER_THRESHOLD_LOW", "0.40"))
DEFER_THRESHOLD_HIGH = float(os.getenv("DEFER_THRESHOLD_HIGH", "0.60"))

RAW_DATASET_PATH = BASE_DIR / os.getenv(
    "RAW_DATASET_PATH", "ml/data/raw/emscad_research_ready.csv"
)
