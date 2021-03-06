"""
Django settings for backend project.

Generated by "django-admin startproject" using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mn$r09=&b86hi39y0@(#ws*mnlg!qy_u5kk1(61ps-bho2bbf9"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    #third party apps

    "crispy_forms",
    # "crispy_bootstrap5",
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    # 'online_users',

    #local apps

    "core",
    "map",
    "users",
    "api",
    "notifications"
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# MIDDLEWARE_CLASSES = (
#     'online_users.middleware.OnlineMiddleware'
# )

ROOT_URLCONF = "backend.urls"
ASGI_APPLICATION = 'backend.routing.application'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/"templates"],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR/"static/",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# API = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg" or "AIzaSyB8L1CtMqsKVbSMT2SWvXgNLzboRDNcvhg"

MB_ACCESS_TOKEN = "pk.eyJ1IjoiaXZhbnRvbSIsImEiOiJjbDJnMGlwNnYwZm9zM2duYnQ0a3c2bXFvIn0.x29uaFl79xgLW6nCs15JWw" # mapbox
GA_ACCESS_TOKEN = 'f510ff426d79491d94496a072fbf8841' # geoapify
MQ_ACCESS_TOKEN = 'UctpoKg4IqAjvPhGdGfjtAluiLhEXobt' # mapquest
PS_ACCESS_TOKEN = '2b6e5e6ef48e5c6a8ec62a0f8c48e3d3' # position stack

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'index'

#Adding bootstrap to my project through crispy forms

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap4"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
