from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-gwupewp@i(5na=%45p^&9da3kaglz4@180^ncqz$l64vssu_n7'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cm_site.apps.CmSiteConfig',
    # Надстройка для allauth
    'django.contrib.sites',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# django-allouth

# email обязателен
ACCOUNT_EMAIL_REQUIRED = True

# Дней на подтверждения email
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

# Максимальная длина имени
ACCOUNT_USERNAME_MAX_LENGTH = 25

# Уникальный email
ACCOUNT_UNIQUE_EMAIL = True

# хз
ACCOUNT_EMAIL_VERIFICATION_METHOD = 'email'

# Задний привод allauth регестрации
AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'social_core.backends.vk.VKOAuth2',
}

# Переменная 'django.contrib.sites'
SITE_ID = 1

# время хранения сессии (сейчас == 30 лет) ((60 * 60 * 24 * 30 * 12) *30)
SESSION_COOKIE_AGE = 31104000 * 30

# Дополнение к стандартной таблице User
AUTH_USER_MODEL = 'cm_site.CustomUser'  

# Перенаправление после входа
LOGIN_REDIRECT_URL = '/store/'

# Перенаправление после выхода
ACCOUNT_LOGOUT_REDIRECT_URL = '/store/'

# Перенаправление после подтверждения email
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/store/'

# подтверждение по email обязательно
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Метод подтверждения email
ACCOUNT_AUTHENTICATION_METHOD  = 'username_email'

# Настройки отправки писем
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Отправкой через Gmail SMTP сервер
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if DEBUG:
    EMAIL_HOST_USER = 'inco.k.b.blizz@gmail.com'
    EMAIL_HOST_PASSWORD = 'ltzw ivpx tqib lxnl'
else:
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''


ROOT_URLCONF = 'settings.urls'
#end django-allouth

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # middleware allauth
    'allauth.account.middleware.AccountMiddleware',
]

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

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


