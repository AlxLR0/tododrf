"""
🧩 tododrf / settings.py
Configuración principal del proyecto Django.
Aquí se define todo: apps instaladas, base de datos, middleware, auth con JWT, etc.
"""

from pathlib import Path

# ── Ruta base del proyecto ──
# BASE_DIR apunta a la raíz (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q59wap@y-^q6qce^00ufr!4doem#tmna@+_64k2^1&$%e_hek5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 🚨 Modo desarrollo — CAMBIAR a False en producción

ALLOWED_HOSTS = []  # 📝 Acá van los dominios permitidos en prod


# Application definition

INSTALLED_APPS = [
    # 📦 Apps nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 📦 Apps de terceros
    'rest_framework',      # 🔌 Django REST Framework
    # 📦 Apps propias
    'tasks'                # ✅ Nuestra app de tareas
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # ── Auth / Mensajes ──
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 📍 El archivo que contiene las rutas raíz (urls.py de tododrf/)
ROOT_URLCONF = 'tododrf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tododrf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # 🗄️ SQLite para dev
        'NAME': BASE_DIR / 'db.sqlite3',          # 📁 El archivo db.sqlite3
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # 🔐 Validadores de seguridad para contraseñas
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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'     # 🌐 Idioma
TIME_ZONE = 'UTC'           # 🕐 Zona horaria
USE_I18N = True             # 🌍 Activar internacionalización
USE_TZ = True               # 🕐 Usar timezone-aware datetimes


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'  # 🖼️ URL para archivos estáticos



# ⚙️ Configuración de Django REST Framework
REST_FRAMEWORK ={
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 🔑 Autenticación via JWT (simplejwt)
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 🚪 Por defecto, todo requiere usuario autenticado
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 📄 Paginación global
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2  # 📏 2 items por página
}