"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import logging
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

import django_heroku

#####

from rich.traceback import install
install()

#####

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        "rich": {
            "datefmt": "[%x %X]"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'rich.logging.RichHandler',
            'formatter': 'rich',
            'rich_tracebacks': True,
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}


def _require_env(name):
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured(
            'Required environment variable "{}" is not set.'.format(name))
    return value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!

if os.environ.get('DJANGO_DEBUG', False):
    DEBUG = True
    SECRET_KEY = '2_86tnhr%jt4=on%gks(f7k^s_)wm938khqjmrnsljzvt^_=jf'
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "ngrok.io"]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
    SECURE_SSL_REDIRECT = False
    print("DEBUG IS ON!")
else:
    DEBUG = False
    SECRET_KEY = _require_env('SECRET_KEY')
    ALLOWED_HOSTS = ['*']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    print("DEBUG IS OFF!")


# Application definition

INSTALLED_APPS = [
    'kmuhelper'

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'multi_email_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_PANELS = [
        # 'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        # 'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        # 'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        # 'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        # 'SHOW_TOOLBAR_CALLBACK': lambda r: False,
        # Uncomment to hide toolbar
    }

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'mysite' / 'templates',
        ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# TODO: Configure Database (Uncomment one of these 2 or use your own)

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'mydatabase',
    # },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': _require_env('DB_HOST'),
    #     'USER': _require_env('DB_USER'),
    #     'PASSWORD': _require_env('DB_PASSWORD'),
    #     'NAME': _require_env('DB_NAME'),
    #     'PORT': os.getenv('DB_PORT', 3306),
    #     "OPTIONS": {
    #         "charset": "utf8mb4",
    #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    #     },
    # }
}

# TODO: Configure E-Mail

EMAIL_HOST = os.getenv("EMAIL_HOST", "asmtp.mail.hostpoint.ch")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = ""

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Format "NAME <E-Mail>" or "E-Mail"
SERVER_EMAIL = EMAIL_HOST_USER  # Format "NAME <E-Mail>" or "E-Mail"

ADMINS = [
    # ("Webmaster", "webmaster@example.com")
]
MANAGERS = [
    # ("Service", "service@example.com")
]

LOGIN_URL = reverse_lazy("admin:login")

# KMUHelper Config

## Used for 'view online' URLs in E-Mails
#KMUHELPER_DOMAIN = "https://example.com"

## Add this address as BCC to every outgoing email
#KMUHELPER_LOG_EMAIL = "log@example.com"

## Add this default context to every email
#KMUHELPER_EMAILS_DEFAULT_CONTEXT = {
#    "precontent": "",
#    "postcontent": """freundliche Grüsse\n\nIhre Firma""",
#    "header_background": "#AA1155",
#    "header_foreground": "#FFEE88",
#    "header_title": "KMUHelper | E-Mails",
#}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'de-CH'
TIME_ZONE = 'Europe/Zurich'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage '

STATICFILES_DIRS = [
    BASE_DIR / 'mysite' / 'static'
]


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Configure Django App for Heroku.
django_heroku.settings(locals(), logging=False)
