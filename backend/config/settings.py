"""
Django settings for ResumeIQ MVP.
"""

from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-dev-key'
)

DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)

# =========================
# HOSTS
# =========================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "resumeiq-production.up.railway.app"
]


# =========================
# INSTALLED APPS
# =========================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'apps.users',
    'apps.resumes',
    'apps.jobs',
    'apps.analysis',
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND':
        'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# =========================
# DATABASE
# =========================

DATABASES = {

    'default': {

        'ENGINE':
        'django.db.backends.sqlite3',

        'NAME':
        BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# PASSWORD VALIDATORS
# =========================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    }

]


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================
# STATIC FILES
# =========================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# =========================
# MEDIA
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =========================
# USER MODEL
# =========================

AUTH_USER_MODEL = 'users.CustomUser'


# =========================
# REST FRAMEWORK
# =========================

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

    'DEFAULT_PERMISSION_CLASSES': (

        'rest_framework.permissions.IsAuthenticated',

    )
}


# =========================
# JWT
# =========================

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME':
    timedelta(hours=24),

    'REFRESH_TOKEN_LIFETIME':
    timedelta(days=7),

    'ROTATE_REFRESH_TOKENS':
    True,
}


# =========================
# CORS
# =========================

# Temporary debugging mode
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# =========================
# FILE UPLOAD
# =========================

MAX_UPLOAD_SIZE = 10 * 1024 * 1024

SUPPORTED_RESUME_FORMATS = [
    'pdf',
    'docx'
]


# =========================
# CACHE
# =========================

CACHES = {

    "default": {

        "BACKEND":
        "django.core.cache.backends.locmem.LocMemCache",
    }
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'