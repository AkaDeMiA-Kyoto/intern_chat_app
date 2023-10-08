"""
Django settings for intern project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os 
import environ 
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ozyl(r!*=wht$a7^pp+wp=zg5g96yg5wz!7fwe$gq63874z9##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# タイムゾーンを日本に
TIME_ZONE = 'Asia/Tokyo'

# 原語を日本語に
LANGUAGE_CODE = 'ja'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'django.contrib.sites',    
    'allauth',     
    'allauth.account',     
    'allauth.socialaccount',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'intern.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'accounts/templates'),
        ],
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

WSGI_APPLICATION = 'intern.wsgi.application'


# 
# base
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database',
        'USER': 'fukurohoho',
        'PASSWORD': 'honokasanda',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length' : 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # 数値のみでパスワードが構成されていないか確認する
    },
]
# https://shelokuma.com/2021/07/22/how-to-use-validation-for-login-password/

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/myapp/static/'
STATIC_ROOT = BASE_DIR / "myapp/static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# signup form
MEDIA_URL = '/media_local/'
MEDIA_ROOT = BASE_DIR / 'media_local'
AUTH_USER_MODEL = "myapp.CustomUser"
ACCOUNT_FORMS   = { "signup":"myapp.forms.myUserForm"}

# デプロイ環境のための設定(追加)
if os.path.isfile('.env'): # .envファイルが存在しない時にもエラーが発生しないようにする
    env = environ.Env(DEBUG=(bool, False),)
    environ.Env.read_env('.env')

    DEBUG = env('DEBUG')
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# django-allauth を使うための設定
AUTHENTICATION_BACKENDS = [ 
  'django.contrib.auth.backends.ModelBackend',     
  'allauth.account.auth_backends.AuthenticationBackend',
] 

SITE_ID = 1

#コンソール上にユーザ登録確認メールを表示。ローカルで確認するため
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

#django-allauthログイン時とログアウト時のリダイレクトURL
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = 'email'

#ユーザ登録確認メールを送信
ACCOUNT_EMAIL_VARIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

SIGNUP_REDIRECT_URL = "/"
LOGIN_URL = '/login'

#signupformからの情報をcustomusermodelに保存するのに必要
ACCOUNT_ADAPTER = 'myapp.adapter.AccountAdapter'

LOGIN_REDIRECT_URL="/friends"
