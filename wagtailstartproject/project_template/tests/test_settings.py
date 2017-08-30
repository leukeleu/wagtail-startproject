import logging

from {{ project_name }}.settings import *  # noqa

logging.disable(logging.CRITICAL)

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}',
        'USER': 'postgres'
    },
}

# Add middleware to add a meta tag with the response status code for Selenium
MIDDLEWARE += [  # noqa: F405
    'tests.middleware.PageStatusMiddleware'
]

# Fixture location
FIXTURE_DIRS = ['tests/fixtures/']

# Set the default cache to be a dummy cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Use dummy backend for safety and performance
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Disable the automatic indexing (sigals) of your search backend
# In WAGTAILSEARCH_BACKENDS set AUTO_UPDATE for each backend to False
