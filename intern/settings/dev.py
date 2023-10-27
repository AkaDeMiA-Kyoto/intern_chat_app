import os

from .base import *
DEBUG = os.getenv("DEBUG", "y")

CORS_ALLOW_ALL_ORIGINS = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}