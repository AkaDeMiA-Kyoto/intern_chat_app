import os 
from .common import *
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "postgres",
        'USER': "ryusei",
        'PASSWORD': "abe1640bom",
        'HOST': "localhost", 
        'PORT': "5432",
    }
}


