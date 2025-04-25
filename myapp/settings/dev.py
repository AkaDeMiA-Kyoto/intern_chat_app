import os

from .base import *
from .utils import strtobool

#DEBUG = strtobool(os.getenv("DEBUG", "y"))
DEBUG = True
CORS_ALLOW_ALL_ORIGINS = DEBUG