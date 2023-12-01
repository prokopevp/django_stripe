import socket

from simple_solutions_stripe.settings import *

DEBUG = False

ALLOWED_HOSTS = list(os.environ['ALLOWED_HOSTS'].split(' '))
CSRF_TRUSTED_ORIGINS = list(os.environ['CSRF_TRUSTED_ORIGINS'].split(' '))
CSRF_COOKIE_SECURE = False
USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # Используется PostgreSQL
        'NAME': os.environ['DB_NAME'], # Имя базы данных
        'USER': os.environ['DB_USER'], # Имя пользователя
        'PASSWORD': os.environ['DB_PASSWORD'], # Пароль пользователя
        'HOST': os.environ['DB_HOST'], # Наименование контейнера для базы данных в Docker Compose
        'PORT': os.environ['DB_PORT'],  # Порт базы данных
    }
}
