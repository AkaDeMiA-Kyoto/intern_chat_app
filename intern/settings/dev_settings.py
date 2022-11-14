import os

from dotenv import load_dotenv

from .base_settings import *

load_dotenv(".env")

DEBUG = os.getenv("DEBUG")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('USER_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# python manage.py runserver --settings intern.settings.dev_settings 
