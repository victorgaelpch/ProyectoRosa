from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cg5c4s=d0o@y&-&hbvdq&k_ob!hw0gm_7f$-h0t8g222f00@bv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # local apps
    'miInicio',
    'pedido',
    'perfil',
    'menu',
    'administracion',
    'gestion',
    'caja',

]


INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SisWebCafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'SisWebCafe.context_processors.es_gerente',
            ],
        },
    },
]

WSGI_APPLICATION = 'SisWebCafe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
# Configuración de la base de datos PostgreSQL
DATABASES = {
    'default': {  # Para escrituras (Master)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafebd',
        'USER': 'postgres',
        # 'USER': 'usuario_lectura',
        'PASSWORD': 'tamalitoUaemex',
        'HOST': '187.221.22.67',  # Ej: 192.168.1.101
        'PORT': '5432',  # Puerto del Master en HAProxy
    },
    'read': {  # Para lecturas (Slaves)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafebd',
        'USER': 'postgres',
        # 'USER': 'usuario_lectura',
        'PASSWORD': 'tamalitoUaemex',
        'HOST': '187.221.22.67',
        'PORT': '5433',  # Puerto de Slaves en HAProxy
    }
}
# Router para manejar lecturas/escrituras
DATABASE_ROUTERS = ['SisWebCafe.routers.PrimaryReplicaRouter']
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
"""
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = 'home'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
