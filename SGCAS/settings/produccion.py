from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sgcas.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #
    #     'NAME': 'damj5k2s7el799',
    #     'USER': 'qjrltnycoqigoz',
    #     'PASSWORD': '03e10c13eec96b237f23b64b7c1c2408813a52bc4925c756b59e2198486b2101',
    #     'HOST': 'ec2-34-238-26-109.compute-1.amazonaws.com',
    #     'PORT': 5432,
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'produccion',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# STATICFILES_DIRS = (BASE_DIR, 'static')
# STATIC_ROOT = os.path.join("static/")
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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