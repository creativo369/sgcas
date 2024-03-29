"""
Django settings for SGCAS project.

Generated by 'django-admin startproject' using Django 3.0.4.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
>>>>>>> 2ee7ce8d840f9c6c7063671e42c3ba744a7e4991
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print ("base dir path", BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'nayi!!*seyd)t#+m)2@l&7m3^!6j=*$vytuxb86ig1#pq(=khl'

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
    'apps.usuario',
    'apps.proyecto',
    'apps.fase',
    'apps.linea_base',
    'apps.comite',
    'apps.rol',
    'apps.tipo_item',
    'apps.item',
    'apps.mensajes',
    'multiselectfield',
    'guardian',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'import_export',
    'finalware',
]

AUTH_USER_MODEL = 'usuario.User'
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.usuario.middleware.RolMiddleware',

]

ROOT_URLCONF = 'SGCAS.urls'

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDusx5xjeTHzgEFWGrhN-YK_rvqFt2F8QM",
    "authDomain": "sgcas-is2-team7.firebaseapp.com",
    "databaseURL": "https://sgcas-is2-team7.firebaseio.com",
    "projectId": "sgcas-is2-team7",
    "storageBucket": "sgcas-is2-team7.appspot.com",
    "messagingSenderId": "87120322887",
    "appId": "1:87120322887:web:7864648c8b0706afcfac62"
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.mensajes.context_processors.count_inactive_users'

            ],
        },
    },
]

WSGI_APPLICATION = 'SGCAS.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'developersIS2',
#         'USER': 'postgres',
#         'PASSWORD': 'admin',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     },
#     # 'production': {
#     #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     #     'NAME': 'production',
#     #     'USER': 'postgres',
#     #     'PASSWORD': 'admin',
#     #     'HOST': 'localhost',
#     #     'PORT': 5432,
#     # },
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # Configuracion necesaria para el guardian
    'guardian.backends.ObjectPermissionBackend',
)

LOGIN_URL = '/account/login'

# La url a donde se dirige una vez realizado el login
LOGIN_REDIRECT_URL = '/usuario'

# The URL (or URL name) to return to after the user logs out. This is the counterpart to Django’s
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# The user is required to hand over an e-mail address when signing up.
# ACCOUNT_EMAIL_REQUIRED = True

# When set to “mandatory” the user is blocked from logging in until the email address is verified.
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# The user is required to enter a username when signing up.
# s ACCOUNT_USERNAME_REQUIRED = True

# Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider.
# SOCIALACCOUNT_AUTO_SIGNUP = False

# Indicates whether or not the access tokens are stored in the database.

# SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# el alcance del correo electrónico para recibir las direcciones de correo electrónico
# del usuario después de un inicio de sesión social exitoso

# Configuraciones para el envio de mail
# Configuraciones para el envio de email a traves de gmail en producción y consola en desarrollo
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'is2.equipo7.sgcas@gmail.com'
EMAIL_HOST_PASSWORD = 'is212345678'
EMAIL_PORT = 587

# To create/update a superuser account automatically, add the following to your settings file.
# This will disable the `superuser` creation option of syncdb.

# This field is stored in `User.USERNAME_FIELD`. This is usually a `username` or  an `email`.
SITE_SUPERUSER_USERNAME = 'AdminDjango'

# This field is stored in the `email` field, provided, that `User.USERNAME_FIELD` is not an `email`.
# If `User.USERNAME_FIELD` is already an email address, set `SITE_SUPERUSER_EMAIL = SITE_SUPERUSER_USERNAME`
SITE_SUPERUSER_EMAIL = ''

# A hashed version of `SITE_SUPERUSER_PASSWORD` will be store in superuser's `password` field.
SITE_SUPERUSER_PASSWORD = 'qwertydjango'

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)
