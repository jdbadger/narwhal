from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if not all((AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)):
    STORAGES['default'] = {
        'BACKEND': 'django.core.files.storage.InMemoryStorage'
    }
    STORAGES['private'] = STORAGES['default']
    STORAGES['public'] = STORAGES['default']

# django-debug-toolbar
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar', ]
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
# NOTE:
# The below snippet is the officially recognized method to configure INTERNAL_IPS for
# Django Debug Toolbar when using docker.
# See: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
#
# import socket  # only if you haven't already imported this
# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
#
# For some as yet undetermined reason, this snippet has stopped working (possibly due to docker changes).
# See: https://github.com/jazzband/django-debug-toolbar/issues/1854
#
# The below configuration is temporary solution and will be updated at such time an official solution
# is documented in the debug toolbar docs.
# See: https://django-debug-toolbar.readthedocs.io/en/latest
INTERNAL_IPS = type("c", (), {"__contains__": lambda *a: True})()
