"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

import json
import os

from configparser import ConfigParser

# Default and local config files can be found here
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(PACKAGE_DIR)

# Get config files. Get file given by env variable APP_SETTINGS and local.ini.
# The settings in local.ini overwrite any set in the APP_SETTINGS file.
config = ConfigParser(converters={'literal': json.loads}, interpolation=None)
config.read([
    os.environ.get('APP_SETTINGS', os.path.join(PACKAGE_DIR, 'local.ini')),
    os.path.join(PACKAGE_DIR, 'local.ini'),
])

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.getliteral('app', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('app', 'debug', fallback=False)

ALLOWED_HOSTS = config.getliteral('app', 'allowed_hosts')

# Application definition

INSTALLED_APPS = [
    '{{ project_name }}',
    '{{ project_name }}.pages',
    '{{ project_name }}.search',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PACKAGE_DIR, 'templates'),
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

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': config.getliteral('app', 'db_host', fallback=''),
        'NAME': config.getliteral('app', 'db_name'),
        'USER': config.getliteral('app', 'db_user'),
        'PASSWORD': config.getliteral('app', 'db_password'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PACKAGE_DIR, 'static'),
]

STATIC_URL = '/static/'
if DEBUG:
    # STATIC_ROOT defaults to BASE_DIR/var/staticfiles in debug mode
    STATIC_ROOT = config.getliteral('app', 'static_root', fallback=os.path.join(BASE_DIR, 'var', 'staticfiles'))
else:
    # Require STATIC_ROOT to be configured
    STATIC_ROOT = config.getliteral('app', 'static_root')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "{{ project_name }}"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
# BASE_URL = 'http://example.com'
