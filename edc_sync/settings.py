"""
Django settings for bcpp_interview project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4w#xs+=lrx4$mmqv+vzy^9i!(sni2eh=q_-9(#w4r20sv($2af'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_revision',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_framework_swagger',
    'django_crypto_fields.apps.AppConfig',
    'django_js_reverse',
    'simple_history',
    'edc_appointment.apps.AppConfig',
    'edc_base.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_sync_files.apps.AppConfig',
    # 'edc_lab.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    'edc_offstudy.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_visit_tracking.apps.AppConfig',
    'edc_example.apps.AppConfig',
    'edc_sync.apps.AppConfig',
]

if 'test' in sys.argv:
    # Ignore running migrations on unit tests -- speeds up tests.
    MIGRATION_MODULES = {
        "call_manager": None,
        "edc_appointment": None,
        "edc_code_lists": None,
        "edc_configuration": None,
        "edc_consent": None,
        "edc_content_type_map": None,
        "edc_data_manager": None,
        "edc_death_report": None,
        "edc_death_report": None,
        "edc_identifier": None,
        "edc_metadata": None,
        "edc_registration": None,
        "edc_sync": None,
        "edc_visit_schedule": None,
        "edc_visit_tracking": None,
        "edc_lab": None,
        "edc_sync_files": None,
        "ba_namotswe": None,
        'django_crypto_fields': None,
    }

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django-crossdomainxhr-middleware.XsSharing',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'edc_sync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'edc_sync.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    # required for tests when acting as a server that deserializes
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # required for tests when acting as a server but not attempting to deserialize
    'server': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # required for tests when acting as a client
    'client': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'test_server': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('static')
MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


GIT_DIR = BASE_DIR.ancestor(1)
KEY_PATH = os.path.join(BASE_DIR.ancestor(1), 'crypto_fields')
EDC_CRYPTO_FIELDS_CLIENT_USING = 'client'
SHOW_CRYPTO_FORM_DATA = True

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)
DEVICE_ID = '15'
SERVER_DEVICE_ID_LIST = ['99']
# MIDDLEMAN_DEVICE_ID_LIST = []

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'edc_sync.auth.EdcSyncSignatureAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     )
}


APP_LABEL = 'edc_sync'
