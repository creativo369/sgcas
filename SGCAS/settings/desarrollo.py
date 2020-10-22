from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# STATICFILES_DIRS = (BASE_DIR, 'static')
# STATIC_ROOT = os.path.join("static/")
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "SGCAS", "deployment", "collected_static")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "SGCAS", "deployment", "media")
# print(MEDIA_ROOT,STATIC_ROOT,STATICFILES_DIRS,STATIC_URL,MEDIA_URL)
# └── SGCAS
#     └── BASE_DIR
#         ├── SGCAS
#         │   │
#         │   │── settings
#         │   │  ├──base.py
#         │   │  ├──desarrollo.py
#         │   │  ├──produccion.py
#         │   └── static            -> STATICFILES_DIRS
#         ├── manage.py
#         └── deployment
#             ├── collected_static  -> STATIC_ROOT
#             └── media             -> MEDIA_ROOT
