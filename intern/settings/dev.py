# 開発環境用設定

import os

from .base import *  

DEBUG = os.getenv("DEBUG", "y")

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

# debug-toolbar 導入用
INTERNAL_IPS = ['127.0.0.1']

# debug-toolbar 導入用
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : lambda request: True,
}
