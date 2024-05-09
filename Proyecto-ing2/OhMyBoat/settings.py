"""
Django settings for OhMyBoat project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o-vxt$06qs$!m=m-1y3qfh%0*0s2-6@#@_223jp%th-$1s8&c8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'autenticacion',
    'inicio',
    'administrador',
    'empleados',
    'embarcaciones'
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

ROOT_URLCONF = 'OhMyBoat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'autenticacion/templates'),os.path.join(BASE_DIR,'inicio/templates')
                 ,os.path.join(BASE_DIR,'administrador/templates'),os.path.join(BASE_DIR, 'embarcaciones/templates')],
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

WSGI_APPLICATION = 'OhMyBoat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators



# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inicio/static'),
    os.path.join(BASE_DIR, 'autenticacion/static'),
    os.path.join(BASE_DIR, 'embarcaciones/static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'embarcaciones/imagenes_embarcaciones')
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#tiempo para que se expire la sesion
#funciona mal a chekear
#SESSION_COOKIE_AGE = 600

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTHENTICATION_BACKENDS = ['autenticacion.backend.UsuarioBackend']

AUTH_USER_MODEL = 'usuarios.Usuario'

#Credenciales del servidor de correo

EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ohmyboat.mail@gmail.com'
EMAIL_HOST_PASSWORD = 'lwzt ctcm nozd rkhn' #Clave de la cuenta de correo para poder acceder desde el programa, habria que encriptarla o guardarla en otro lado
EMAIL_USE_TLS = True