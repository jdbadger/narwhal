import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

import environ
from huey import RedisHuey
from redis import ConnectionPool


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# load variables from .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# default is False
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(" ")

# Application definition

INTERNAL_APPS = [
    'users',
]

THIRD_PARTY_APPS = [
    'huey.contrib.djhuey'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *INTERNAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {'default': env.db()}
DATABASES['default']['CONN_MAX_AGE'] = 60
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Cache
# https://docs.djangoproject.com/en/4.2/ref/settings/#caches

CACHES = {'default': env.cache()}

# Huey

HUEY_URL = env('HUEY_URL')
HUEY_NAME = DATABASES['default']['NAME']
CONNECTION_POOL = ConnectionPool.from_url(HUEY_URL, max_connections=20)
HUEY = RedisHuey(HUEY_NAME, connection_pool=CONNECTION_POOL)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Storages
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES

STORAGES = {
    "default": {
        "BACKEND": 'django.core.files.storage.FileSystemStorage',
    },
    "staticfiles": {
        "BACKEND": 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES['staticfiles'] = {
    # Static files served via Whitenoise (compressed and cached)
    # https://github.com/evansd/whitenoise/blob/main/docs/django.rst
    'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
}

# s3

AWS_ACCESS_KEY_ID = env.get_value('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env.get_value('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = env.get_value(
    'AWS_STORAGE_BUCKET_NAME', default=None)
if all((AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)):
    STORAGES['default'] = {'BACKEND': 'utils.storages.S3StoragePrivate'}
    STORAGES['private'] = {'BACKEND': 'utils.storages.S3StoragePrivate'}
    STORAGES['public'] = {'BACKEND': 'utils.storages.S3StoragePublic'}

# Custom User Model

AUTH_USER_MODEL = 'users.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
