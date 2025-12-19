import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'
PROD = os.getenv('PROD', 'False') == 'True'

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://gestao.meganetrio.com.br']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'main.apps.pay',
    'main.apps.home',
    'main.apps.account',
    # external apps
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# save Celery task results in Django's database
result_backend = "django-db"
result_extended = True
broker_connection_retry_on_startup = True

# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_REDIS_URL')

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_RESULT_BACKEND = 'django-db'


# Configurar o fuso horário no Celery
CELERY_TIMEZONE = 'America/Sao_Paulo'  
CELERY_ENABLE_UTC = True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# LOGIN
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

LANGUAGE_CODE = 'pt-BR'
USE_I18N = True

TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# LOGIN
LOGOUT_REDIRECT_URL = '/accounts/login/'

# E adicione esta configuração se necessário
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


'''  instancia de alertas '''

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTIONMASTERKEY = os.getenv("EVOLUTIONMASTERKEY")

INSTANCE_NAME = os.getenv("INSTANCE_NAME")
INSTANCE_KEY = os.getenv("INSTANCE_KEY")
INSTANCE_NUMBER = os.getenv ("INSTANCE_NUMBER")