import os

from .base import *
from .utils import strtobool

DEBUG = strtobool(os.getenv("DEBUG", "y"))

CORS_ALLOW_ALL_ORIGINS = DEBUG

ROOT_URLCONF = 'intern.urls'
