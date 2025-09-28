from dotenv import load_dotenv
from .base import *
import os
load_dotenv()

SECRET_KEY = 'oaab#2kr%trbj2h-w9ycf0&f$7dgi2+p=37!cjw$*y0@26pq77'

DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
