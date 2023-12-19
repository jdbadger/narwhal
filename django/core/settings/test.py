from .base import *

from django.core.management.utils import get_random_secret_key


DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = get_random_secret_key()

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

STORAGES['default'] = {
    'BACKEND': 'django.core.files.storage.InMemoryStorage'
}
STORAGES['private'] = STORAGES['default']
STORAGES['public'] = STORAGES['default']
