"""
Django settings for ProyectoTikTok project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.messages import constants as mensajes_de_error
from ProyectoTikTok.config import HOTMAIL

# Importa la configuración de django-crispy-forms
# from django.conf.global_settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#hisz8p_j-58*7+1nlh=!r5ri@cu5hxolce+g&jf*oo^=s6^u2'

# SECURITY WARNING: don't run with debug turned on in production!
# Cambiar a False cuando este en produccion
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'usuario',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'video_tiktok',

    'crispy_forms',
    'crispy_bootstrap5',
    'accounts',
    # 'ZoomVideoComposer',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LANGUAGE_CODE = 'es'

# VARIABLES DE REDIRECCION DE LOGIN Y LOGOUT
LOGIN_REDIRECT_URL = 'index'
# LOGOUT_REDIRECT_URL = 'index'

# proteger a tus usuarios de ataques de falsificación de solicitudes entre sitios.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', #  middleware de sesiones habilitado
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProyectoTikTok.urls'

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
                'usuario.context_processors.creditos_usuario',

            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoTikTok.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bdclientes',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'video_tiktok', 'static')]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Tiempo de Vida de la Sesión
#SESSION_COOKIE_AGE = 1200  # 20 minutos, por defecto sera de 2 semanas
SESSION_COOKIE_AGE = 1209600  # Duración de la sesión en segundos (2 semanas)
# Hacer que las sesiones caduquen cuando el usuario cierre el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True  # Guardar la sesión en cada solicitud, incluso si no ha cambiado
# Si tu aplicación usa HTTPS (en producción),
# asegura que las cookies de sesión solo se transmitan a través de conexiones seguras:
# SESSION_COOKIE_SECURE = True


# Activar en entorno de producción: ejecutar python manage.py collectstaticpara que Django recoja todos sus archivos estáticos y los coloque en la carpeta collected_static.
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / 'collected_static' # recopila todos tus archivos estáticos para que puedan ser servidos por tu servidor web


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USO de almacenamiento local por defecto que ofrece Django
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'usuario.UsuarioPersonalizado'

'''
# Recupero de contraseña: almacenaremos todos los correos electrónicos enviados en una carpeta llamada en nuestro
# directorio de proyectos.sent_emails
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend" # el backend basado en archivos o
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
else:
    #Configurar email real para produccion
    pass

# Configuracion de GMAIL
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # el backend SMTP.
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'giuly03@hotmail.com'
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True

'''
# Configuracion de HOTMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # el backend SMTP.
EMAIL_HOST = 'smtp-mail.outlook.com' # servidor SMTP de Hotmail
EMAIL_PORT = 587 #465
EMAIL_HOST_USER = 'giuly03@hotmail.com'
EMAIL_HOST_PASSWORD = HOTMAIL
DEFAULT_FROM_EMAIL = 'giuly03@hotmail.com'
EMAIL_USE_TLS = True

MESSAGE_TAGS={
    mensajes_de_error.DEBUG: 'debug',
    mensajes_de_error.INFO: 'info',
    mensajes_de_error.SUCCESS: 'success',
    mensajes_de_error.WARNING: 'warning',
    mensajes_de_error.ERROR: 'danger',

    }
