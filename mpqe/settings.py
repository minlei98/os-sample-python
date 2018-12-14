"""
Django settings for mpqe project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import configparser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (BASE_DIR) 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-1b1b&c%d=e#7sbq(ft_b&q_mfeteo)r6abqck%#rdz&meo0fn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# increment and set for every release!
RELEASE_VERSION = '0.5.8'

config = configparser.RawConfigParser()
config.read(os.path.join(BASE_DIR, 'mpqe_setup.cfg'))
DEPLOYMENT = config.get('general', 'mpqe_deployment_type').upper()
MPQE_HOST = config.get('mpqe', 'mpqe_host')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    MPQE_HOST,
    '*'
]




# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'rest_framework', 
    'api'
]

# OLD SETTINGS
# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions, or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [ 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly' ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 10
#     
# }

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mpqe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],  
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

WSGI_APPLICATION = 'mpqe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# sqlite3
# DATABASES_SQLITE = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# local devel db 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mpqe_v1',
#         'USER': 'dbuser',
#         'PASSWORD': 'db1$',
#         'HOST': 'localhost',
#         'PORT': 5433
#     }
# }

# prod db
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'interop',
#         'USER': 'dbuser',
#         'PASSWORD': 'db1$',
#         'HOST': '10.8.251.51',
#         'PORT': 5432
#     }
# }


print ('Database Connection Information:',
        config.get('database', 'mpqe_database_type'),
         config.get('database', 'postgres_host'),
          config.get('database', 'postgres_name'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('database', 'postgres_name'),
        'USER': config.get('database', 'postgres_user'),
        'PASSWORD': config.get('database', 'postgres_password'),
        'HOST': config.get('database', 'postgres_host'),
        'PORT': config.get('database', 'postgres_port'),
    }
}




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'
TIME_ZONE = config.get('general', 'mpqe_tz')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # or direct path to static
    # /direct/path/to/static/folder/,
    os.path.join(BASE_DIR, "static", "static"),
    ('images', 'static/images'),
)


# service user
MPQE_SERVICEUSER = 'service_user'
MPQE_SERVICEUSERPW = '1qaz2wsx'

