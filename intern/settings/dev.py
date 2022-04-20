# 開発環境用設定

import os

from .base import *  # noqa: F401,F403
from .utils import strtobool

DEBUG = strtobool(os.getenv("DEBUG", "y"))

CORS_ALLOW_ALL_ORIGINS = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER':  os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}