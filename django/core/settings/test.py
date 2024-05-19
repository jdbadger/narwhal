from .base import *

from django.core.management.utils import get_random_secret_key

ALLOWED_HOSTS = []

DEBUG = True

SECRET_KEY = env.get_value('SECRET_KEY', default=get_random_secret_key())

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

STORAGES['default'] = {'BACKEND': 'django.core.files.storage.InMemoryStorage'}
STORAGES['private'] = STORAGES['default']
STORAGES['public'] = STORAGES['default']
