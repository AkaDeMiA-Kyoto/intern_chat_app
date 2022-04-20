import os
from pathlib import Path

from dotenv import load_dotenv

from .utils import strtobool

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = strtobool(os.getenv("DEBUG", "n"))

ALLOWED_HOSTS = [s.strip() for s in os.getenv("ALLOWED_HOSTS", "").split(",") if s]

CORS_ALLOWED_ORIGINS = [
    s.strip() for s in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if s
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'myapp.apps.MyappConfig',

    # allauth 用の設定
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "intern.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "intern.wsgi.application"

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# User-uploaded files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")


AUTH_USER_MODEL = 'myapp.User'


# django-allauthサイト識別用ID

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend', # 一般ユーザー用(メールアドレス認証)
    'django.contrib.auth.backends.ModelBackend' # 管理サイト用(ユーザー名認証)
)

# メールアドレス認証にする設定

ACCOUNT_AUTHENTICATION_METHOD = 'email'

# サインアップにメールアドレス確認を挟む設定

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True


# ログイン/ログアウト後の遷移先を設定

LOGIN_REDIRECT_URL = '/friends'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'


ACCOUNT_LOGOUT_ON_GET = True  # ログアウトリンクのクリック一発でログアウト
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True # メールアドレスでの確認後即時ログイン

# django-allauthが送信するメールの件名に自動付与される接頭辞をブランクに
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_MAX_EMAIL_ADDRESSES = 2

# allauthのフォームカスタマイズ
ACCOUNT_FORMS = {
    'login': 'myapp.forms.MyLoginForm',
    'signup': 'myapp.forms.MySignupForm',
    'reset_password_from_key': 'myapp.forms.MyResetPasswordKeyForm',
    'reset_password': 'myapp.forms.MyResetPasswordForm',
}

#signupformからの情報をusermodelに保存するのに必要
ACCOUNT_ADAPTER = 'myapp.adapter.AccountAdapter'
