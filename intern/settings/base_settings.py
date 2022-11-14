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
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ['*']


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
    'debug_toolbar',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'intern.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'myapp.User'

# 画像にアクセスするための指定
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ログイン・ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = '/friends'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# email送信設定
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# django_allauth設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    # 一般ユーザ用メールアドレス認証（メールアドレス）
    'django.contrib.auth.backends.ModelBackend'
    # 管理サイト用（ユーザ名認証）
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True

# サインアップにメールアドレス確認を挟むように設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_lOGOUT_ON_GET = True
# メールアドレスでの確認後即時ログイン
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# django-allauthが送信するメールの件名に自動付与される接頭辞をブランクに
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_MAX_EMAIL_ADDRESSES = 2

# allauthのフォームカスタマイズ
ACCOUNT_FORMS = {
    'login': 'myapp.forms.MyLoginForm',
    'signup': 'myapp.forms.MySignUpForm',
    'reset_password_from_key': 'myapp.forms.MyResetPasswordKeyForm',
    # 'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password': 'myapp.forms.MyResetPasswordForm',
}

#signupformからの情報をusermodelに保存するのに必要
ACCOUNT_ADAPTER = 'myapp.adapter.AccountAdapter'

try:
    from .local_settings import *
except ImportError:
    pass

INTERNAL_IPS = ['127.0.0.1']

